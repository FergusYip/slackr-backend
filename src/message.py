'''
Functionality to provide messaging services between users on the program. Will
allow users to send messages, react to messages, pin messages, and alter/remove
their own messages.
'''

import threading
from error import AccessError, InputError
from data_store import DATA_STORE, Message, React
from token_validation import decode_token
import helpers


def message_send(token, channel_id, message, message_id=None):
    '''
    Function that will take in a message as a string
    and append this message to a channel's list of messages.

    Parameters:
        token (str): The user's token to be decoded to get the user's u_id.
        channel_id (int): The channel identification number.
        message (str): The message to be sent in the channel.
        message_id=None: An optional message_id tag default to None for standard messages
                         and given a message_id for the sendlater function.

    Return:
        Dictionary (dict): A dictionary containing one key and value pair of the message_id.
    '''

    if None in {token, channel_id, message}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = DATA_STORE.get_user(u_id)

    channel_id = int(channel_id)
    channel = DATA_STORE.get_channel(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    if len(message) > 1000:
        raise InputError(
            description='Message is greater than 1,000 characters')

    if not message:
        raise InputError(
            description='Message needs to be at least 1 characters')

    hangman_bot_u_id = DATA_STORE.preset_profiles['hangman_bot'].u_id
    if user not in channel.all_members and u_id != hangman_bot_u_id:
        raise AccessError(
            description=
            'User does not have Access to send messages in the current channel'
        )

    msg = Message(user, channel, message, message_id)
    channel.send_message(msg)
    DATA_STORE.add_message(msg)
    user.add_message(msg)

    return {'message_id': msg.message_id}


def message_remove(token, message_id):
    '''
    Function that will take in a message ID and remove this
    message from the list of messages in a specific channel.

    Parameters:
        token (str): The user's token to be decoded to get the user's u_id.
        message_id (int): The message_id of the message that will be removed.

    Return:
        Dictionary (dict): An empty dictionary
    '''

    if None in {token, message_id}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = DATA_STORE.get_user(u_id)

    message_id = int(message_id)
    message = DATA_STORE.get_message(message_id)

    if message is None:
        raise InputError(description='Message does not exist')

    channel = message.channel

    if not (message.u_id == u_id
            or DATA_STORE.is_admin_or_owner(user, channel)):
        raise AccessError(
            description='User does not have access to remove this message')

    if message in channel.messages:
        channel.remove_message(message)

    if message in DATA_STORE.messages:
        DATA_STORE.remove_message(message)

    if message in user.messages:
        user.remove_message(message)

    return {}


def message_edit(token, message_id, message):
    '''
    Function that will take in a new message that will overwrite
    an existing message in a desired channel.

    Parameters:
        token (str): The user's token to be decoded to get the user's u_id.
        message_id (int): The message_id of the message.
        message (str): The message the user will update the current message to.

    Return:
        Dictionary (dict): An empty dictionary
    '''

    if None in {token, message_id, message}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = DATA_STORE.get_user(u_id)

    message_id = int(message_id)
    message_obj = DATA_STORE.get_message(message_id)

    if message_obj is None:
        raise InputError(description='Message does not exist')

    channel = message_obj.channel

    if len(message) > 1000:
        raise InputError(description='Message is over 1,000 characters')

    if not (message_obj.u_id == u_id
            or DATA_STORE.is_admin_or_owner(user, channel)):
        raise AccessError(
            description='User does not have access to remove this message')

    if not message and message_obj in channel.messages:
        channel.remove_message(message_obj)
        user.messages.remove(message_obj)
    else:
        message_obj.edit(message)

    return {}


def message_sendlater(token, channel_id, message, time_sent):
    '''
    Function that will send a message in a desired channel at a specified
    time in the future.

    Parameters:
        token (str): The user's token to be decoded to get the user's u_id.
        channel_id (int): The channel identification number.
        message (str): The message to be sent in the channel.
        time_sent (int): The unix timestamp as an integer of when the message will be sent.

    Return:
        Dictionary (dict): A dictionary containing one key and value pair of the message_id.
    '''

    if None in {token, channel_id, message, time_sent}:
        raise InputError(description='Insufficient parameters')

    decode_token(token)

    channel_id = int(channel_id)
    time_sent = int(time_sent)

    time_now = helpers.utc_now()

    if time_now > time_sent:
        raise InputError(description='Time to send is in the past')

    message_id = DATA_STORE.generate_id('message_id')

    duration = time_sent - time_now
    timer = threading.Timer(duration,
                            message_send,
                            args=[token, channel_id, message, message_id])
    timer.start()

    return {'message_id': message_id}


def message_react(token, message_id, react_id):
    '''
    Function that will add a reaction to a specific message in a desired
    channel.

    Parameters:
        token (str): The user's token to be decoded to get the user's u_id.
        message_id (int): The message_id of the message.
        react_id (int): The type of reaction that will be added to the message.

    Return:
        Dictionary (dict): An empty dictionary
    '''

    if None in {token, message_id, react_id}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    user = DATA_STORE.get_user(token_info['u_id'])

    message_id = int(message_id)
    message = DATA_STORE.get_message(message_id)

    if message is None or message not in user.viewable_messages:
        raise InputError(description='Message does not exist')

    react_id = int(react_id)
    react = message.get_react(react_id)

    channel = message.channel

    if channel.is_member(user.u_id):
        raise InputError(description='User is not in the channel')

    if react_id not in DATA_STORE.reactions.values():
        raise InputError(description='Reaction type is invalid')

    if react is not None:
        if react in user.reacts:
            raise InputError(
                description='User has already reacted to this message')

        react.add_user(user)
        user.add_react(react)
    else:
        react = React(react_id, message)
        message.add_react(react)
        react.add_user(user)
        user.add_react(react)

    return {}


def message_unreact(token, message_id, react_id):
    '''
    Function that will remove a specific reaction from a message in a desired channel.

    Parameters:
        token (str): The user's token to be decoded to get the user's u_id.
        message_id (int): The message_id of the message.
        react_id (int): The type of reaction that will be unreacted from the message.

    Return:
        Dictionary (dict): An empty dictionary
    '''

    if None in {token, message_id, react_id}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    user = DATA_STORE.get_user(token_info['u_id'])

    message_id = int(message_id)
    message = DATA_STORE.get_message(message_id)

    if message is None or message not in user.viewable_messages:
        raise InputError(description='Message does not exist')

    react_id = int(react_id)
    react = message.get_react(react_id)

    channel = message.channel

    if channel.is_member(user.u_id):
        raise InputError(description='User is not in the channel')

    if react_id not in DATA_STORE.reactions.values():
        raise InputError(description='Reaction type is invalid')

    if react is None:
        raise InputError(
            description='Message does not have this type of reaction')

    if user.u_id not in react.u_ids:
        raise InputError(description='User has not reacted to this message')

    if user in react.users:
        react.remove_user(user)
        user.remove_react(react)

    if not react.users:
        message.remove_react(react)

    return {}


def message_pin(token, message_id):
    '''
    Function that will mark a message as 'pinned' to be given special
    display treatment by the frontend.

    Parameters:
        token (str): The user's token to be decoded to get the user's u_id.
        message_id (int): The message_id of the message.

    Return:
        Dictionary (dict): An empty dictionary
    '''

    if None in {token, message_id}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = DATA_STORE.get_user(u_id)

    message_id = int(message_id)
    message = DATA_STORE.get_message(message_id)

    if message is None:
        raise InputError(description='Message does not exist')

    channel = message.channel

    if DATA_STORE.is_admin_or_owner(user, channel) is False:
        raise InputError(
            description='User is not an admin or owner of the channel')

    if message.is_pinned:
        raise InputError(description='Message is already pinned')

    if user not in channel.all_members:
        raise AccessError(description='User is not a member of the channel')

    message.pin()

    return {}


def message_unpin(token, message_id):
    '''
    Function that will remove the 'pinned' status of a message.

    Parameters:
        token (str): The user's token to be decoded to get the user's u_id.
        message_id (int): The message_id of the message.

    Return:
        Dictionary (dict): An empty dictionary
    '''

    if None in {token, message_id}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = DATA_STORE.get_user(u_id)

    message_id = int(message_id)
    message = DATA_STORE.get_message(message_id)

    if message is None:
        raise InputError(description='Message does not exist')

    channel = message.channel

    if DATA_STORE.is_admin_or_owner(user, channel) is False:
        raise InputError(
            description='User is not an admin or owner of the channel')

    if message.is_pinned is False:
        raise InputError(description='Message is not pinned')

    if user not in channel.all_members:
        raise AccessError(description='User is not a member of the channel')

    message.unpin()

    return {}


if __name__ == "__main__":
    pass
