'''
Functionality to provide messaging services between users on the program. Will
allow users to send messages, react to messages, pin messages, and alter/remove
their own messages.
'''

from json import dumps
import threading
from flask import request, Blueprint
from error import AccessError, InputError
from data_store import data_store, Message, React
from token_validation import decode_token
import helpers

MESSAGE = Blueprint('message', __name__)

# ======================================================================
# ======================== FLASK ROUTES ================================
# ======================================================================


@MESSAGE.route("/send", methods=['POST'])
def route_message_send():
    '''
	Flask route to call the message_send function.
	'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    message = payload.get('message')
    return dumps(message_send(token, channel_id, message))


@MESSAGE.route("/remove", methods=['DELETE'])
def route_message_remove():
    '''
	Flask route to call the message_remove function.
	'''
    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    return dumps(message_remove(token, message_id))


@MESSAGE.route("/edit", methods=['PUT'])
def route_message_edit():
    '''
	Flask route to call the message_edit function.
	'''
    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    message = payload.get('message')
    return dumps(message_edit(token, message_id, message))


@MESSAGE.route("/sendlater", methods=['POST'])
def route_message_sendlater():
    '''
	Flask route to call the message_sendlater function.
	'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    message = payload.get('message')
    time_sent = payload.get('time_sent')
    return dumps(message_sendlater(token, channel_id, message, time_sent))


@MESSAGE.route("/react", methods=['POST'])
def route_message_react():
    '''
	Flask route to call the message_react function.
	'''
    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    react_id = payload.get('react_id')
    return dumps(message_react(token, message_id, react_id))


@MESSAGE.route("/unreact", methods=['POST'])
def route_message_unreact():
    '''
	Flask route to call the message_unreact function.
	'''
    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    react_id = payload.get('react_id')
    return dumps(message_unreact(token, message_id, react_id))


@MESSAGE.route("/pin", methods=['POST'])
def route_message_pin():
    '''
	Flask route to call the message_pin function.
	'''

    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    return dumps(message_pin(token, message_id))


@MESSAGE.route("/unpin", methods=['POST'])
def route_message_unpin():
    '''
	Flask route to call the message_unpin function.
	'''

    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    return dumps(message_unpin(token, message_id))


# ======================================================================
# =================== FUNCTION IMPLEMENTATION ==========================
# ======================================================================


def message_send(token, channel_id, message, message_id=None):
    '''
	Function that will take in a message as a string
	and append this message to a channel's list of messages.
	'''

    if None in {token, channel_id, message}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = data_store.get_user(u_id)

    channel_id = int(channel_id)
    channel = data_store.get_channel(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    if len(message) > 1000:
        raise InputError(
            description='Message is greater than 1,000 characters')

    if len(message) == 0:
        raise InputError(
            description='Message needs to be at least 1 characters')

    if user not in channel.all_members:
        raise AccessError(
            description=
            'User does not have Access to send messages in the current channel'
        )

    message = Message(user, channel, message)
    channel.send_message(message)

    return {'message_id': message.message_id}


def message_remove(token, message_id):
    '''
	Function that will take in a message ID and remove this
	message from the list of messages in a specific channel.
	'''

    if None in {token, message_id}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = data_store.get_user(u_id)

    message_id = int(message_id)
    message = data_store.get_message(message_id)

    channel = message.channel

    if message is None:
        raise InputError(description='Message does not exist')

    if not (message.u_id == u_id
            and data_store.is_admin_or_owner(user, channel)):
        raise AccessError(
            description='User does not have access to remove this message')

    if message in channel.messages:
        channel.remove_message(message)

    return {}


def message_edit(token, message_id, message):
    '''
	Function that will take in a new message that will overwrite
	an existing message in a desired channel.
	'''

    if None in {token, message_id, message}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = data_store.get_user(u_id)

    message_id = int(message_id)
    message_obj = data_store.get_message(message_id)

    channel = message_obj.channel

    if message_obj is None:
        raise InputError(description='Message does not exist')

    if len(message) > 1000:
        raise InputError(description='Message is over 1,000 characters')

    if not (message_obj.u_id == u_id
            and data_store.is_admin_or_owner(user, channel)):
        raise AccessError(
            description='User does not have access to remove this message')

    if len(message) == 0 and message_obj in channel.messages:
        channel.remove_message(message_obj)
    else:
        message_obj.message = message

    return {}


def message_sendlater(token, channel_id, message, time_sent):
    '''
	Function that will send a message in a desired channel at a specified
	time in the future.
	'''

    if None in {token, channel_id, message, time_sent}:
        raise InputError(description='Insufficient parameters')

    channel_id = int(channel_id)
    time_sent = int(time_sent)

    time_now = helpers.utc_now()
    if time_now > time_sent:
        raise InputError(description='Time to send is in the past')

    message_id = data_store.generate_id('message_id')

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
	'''
    if None in {token, message_id, react_id}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = data_store.get_user(u_id)

    message_id = int(message_id)
    message = data_store.get_message(message_id)

    react_id = int(react_id)
    react = message.get_react(react_id)

    if message is None or message not in user.viewable_messages:
        raise InputError(description='Message does not exist')

    if react_id not in data_store.reactions.values():
        raise InputError(description='Reaction type is invalid')

    if react is not None:
        if react in user.reacts:
            raise InputError(
                description='User has already reacted to this message')

        react.add_user(user)
        user.add_reacts(react)
    else:
        react = React(react_id, message)
        message.add_react(react)
        react.add_user(user)
        user.add_react(react)

    return {}


def message_unreact(token, message_id, react_id):
    '''
	Function that will remove a specific reaction from a message in a desired channel.
	'''
    if None in {token, message_id, react_id}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = data_store.get_user(u_id)

    message_id = int(message_id)
    message = data_store.get_message(message_id)

    react_id = int(react_id)
    react = message.get_react(react_id)

    if message is None or message not in user.viewable_messages:
        raise InputError(description='Message does not exist')

    if react_id not in data_store.reactions.values():
        raise InputError(description='Reaction type is invalid')

    if react is None:
        raise InputError(
            description='Message does not have this type of reaction')

    if user in react.users:
        react.remove_user(user)
        user.remove_react(react)

    if len(react.users) == 0:
        message.remove_react(react)

    return {}


def message_pin(token, message_id):
    '''
	Function that will mark a message as 'pinned' to be given special
	display treatment by the frontend.
	'''
    if None in {token, message_id}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = data_store.get_user(u_id)

    message_id = int(message_id)
    message = data_store.get_message(message_id)

    channel = message.channel

    if message is None:
        raise InputError(description='Message does not exist')

    if data_store.is_admin_or_owner(user, channel) is False:
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
	'''
    if None in {token, message_id}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = int(token_info['u_id'])
    user = data_store.get_user(u_id)

    message_id = int(message_id)
    message = data_store.get_message(message_id)

    channel = message.channel

    if message is None:
        raise InputError(description='Message does not exist')

    if data_store.is_admin_or_owner(user, channel) is False:
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
