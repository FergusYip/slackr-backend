'''
Functionality to provide messaging services between users on the program. Will
allow users to send messages, react to messages, pin messages, and alter/remove
their own messages.
'''

import threading
from slackr.error import AccessError, InputError
from slackr.token_validation import decode_token
from slackr import helpers
from slackr.models import User, Channel, Message, React
from slackr import db
from slackr.utils.constants import PERMISSIONS, REACTIONS


def message_send(token, channel_id, message):
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
    user = User.query.get(u_id)

    channel_id = int(channel_id)
    channel = Channel.query.get(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    if len(message) > 1000:
        raise InputError(
            description='Message is greater than 1,000 characters')

    if not message:
        raise InputError(
            description='Message needs to be at least 1 characters')

    # hangman_bot_u_id = DATA_STORE.preset_profiles['hangman_bot'].u_id
    if user not in channel.all_members:  # and u_id != hangman_bot_u_id:
        raise AccessError(
            description=
            'User does not have Access to send messages in the current channel'
        )

    msg = Message(message, u_id, channel_id)
    channel.messages.append(msg)
    user.messages.append(msg)
    db.session.add(msg)
    db.session.commit()

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
    user = User.query.get(int(token_info['u_id']))
    message = Message.query.get(int(message_id))

    if message is None:
        raise InputError(description='Message does not exist')

    channel = message.channel

    if not (message.u_id == user.u_id or user.permission_id
            == PERMISSIONS['owner'] or channel.is_owner(user)):
        raise AccessError(
            description='User does not have access to remove this message')

    db.session.delete(message)
    db.session.commit()

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
    user = User.query.get(u_id)

    message_id = int(message_id)
    message_obj = Message.query.get(message_id)

    if message_obj is None:
        raise InputError(description='Message does not exist')

    channel = message_obj.channel

    if len(message) > 1000:
        raise InputError(description='Message is over 1,000 characters')

    if not (message_obj.u_id == u_id or user.permission_id
            == PERMISSIONS['owner'] or channel.is_owner(user)):
        raise AccessError(
            description='User does not have access to remove this message')

    if not message:
        db.session.delete(message_obj)
    else:
        message_obj.message = message

    db.session.commit()

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

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = User.query.get(u_id)

    channel_id = int(channel_id)
    channel = Channel.query.get(channel_id)

    time_sent = int(time_sent)
    time_now = helpers.utc_now()

    if time_now > time_sent:
        raise InputError(description='Time to send is in the past')

    if channel is None:
        raise InputError(description='Channel does not exist.')

    if len(message) > 1000:
        raise InputError(
            description='Message is greater than 1,000 characters')

    if not message:
        raise InputError(
            description='Message needs to be at least 1 characters')

    # hangman_bot_u_id = DATA_STORE.preset_profiles['hangman_bot'].u_id
    if not channel.is_member(user):  # and u_id != hangman_bot_u_id:
        raise AccessError(
            description=
            'User does not have Access to send messages in the current channel'
        )

    msg = Message(message, u_id, channel_id)
    msg.is_hidden = True

    channel.messages.append(msg)
    user.messages.append(msg)

    db.session.add(msg)
    db.session.commit()

    duration = time_sent - time_now
    timer = threading.Timer(duration, show_message, args=[msg])
    timer.start()

    return {'message_id': msg.message_id}


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
    user = User.query.get(token_info['u_id'])

    message_id = int(message_id)
    message = Message.query.get(message_id)

    if message is None:
        raise InputError(description='Message does not exist')

    channel = message.channel

    if not channel.is_member(user):
        raise InputError(description='User is not in the channel')

    if react_id not in REACTIONS.values():
        raise InputError(description='Reaction type is invalid')

    react_id = int(react_id)
    react = message.get_react(react_id)

    if not react:
        react = React(react_id)
        message.reacts.append(react)
        db.session.add(react)
    elif user in react.users:
        raise InputError(
            description='User has already reacted to this reaction')

    react.users.append(user)
    db.session.commit()

    return {}


def message_unreact(token, message_id, react_id):
    '''
    Function that will remove a specific reaction from a message in a desired channel.

    Parameters:
        token (str): The user's token to be decoded to get the user's u_id.
        message_id (int): The message_id of the message.
        react_id (int): The type of reaction that will be removed from the message.

    Return:
        Dictionary (dict): An empty dictionary
    '''

    if None in {token, message_id, react_id}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    user = User.query.get(token_info['u_id'])
    message = Message.query.get(int(message_id))

    if not message:  #or message not in user.viewable_messages:
        raise InputError(description='Message does not exist')

    react = message.get_react(int(react_id))
    channel = message.channel

    if not channel.is_member(user):
        raise InputError(description='User is not in the channel')

    if react_id not in REACTIONS.values():
        raise InputError(description='Reaction type is invalid')

    if react is None:
        raise InputError(
            description='Message does not have this type of reaction')

    if user not in react.users:
        raise InputError(description='User has not reacted to this message')

    react.users.remove(user)

    if not react.users:
        db.session.delete(react)

    db.session.commit()

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
    user = User.query.get(int(token_info['u_id']))
    message = Message.query.get(int(message_id))

    if message is None:
        raise InputError(description='Message does not exist')

    channel = message.channel

    if not (user.permission_id == PERMISSIONS['owner']
            or channel.is_owner(user)):
        raise InputError(
            description='User is not an admin or owner of the channel')

    if message.is_pinned:
        raise InputError(description='Message is already pinned')

    if not channel.is_member(user):
        raise AccessError(description='User is not a member of the channel')

    message.is_pinned = True
    db.session.commit()

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
    user = User.query.get(int(token_info['u_id']))
    message = Message.query.get(int(message_id))

    if message is None:
        raise InputError(description='Message does not exist')

    channel = message.channel

    if not (user.permission_id == PERMISSIONS['owner']
            or channel.is_owner(user)):
        raise InputError(
            description='User is not an admin or owner of the channel')

    if not message.is_pinned:
        raise InputError(description='Message is not pinned')

    if user not in channel.all_members:
        raise AccessError(description='User is not a member of the channel')

    message.is_pinned = False
    db.session.commit()

    return {}


def show_message(message):
    message.is_hidden = False
    message.time_created = helpers.utc_now()
    db.session.commit()


if __name__ == "__main__":
    pass
