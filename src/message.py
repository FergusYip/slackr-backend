'''
Functionality to provide messaging services between users on the program. Will
allow users to send messages, react to messages, pin messages, and alter/remove
their own messages.
'''

import sys
from json import dumps
from flask import Flask, request, Blueprint
from flask_cors import CORS
from error import AccessError, InputError
from data_store import data_store
from token_validation import decode_token
import threading
import helpers

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

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

    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']

    return dumps(message_send(token, channel_id, message))

@MESSAGE.route("/remove", methods=['DELETE'])
def route_message_remove():

    '''
    Flask route to call the message_remove function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])

    return dumps(message_remove(token, message_id))

@MESSAGE.route("/edit", methods=['PUT'])
def route_message_edit():

    '''
    Flask route to call the message_edit function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])
    new_message = payload['message']

<<<<<<< HEAD
    return dumps(message_edit(token, message_id, new_message))

@MESSAGE.route("/sendlater", methods=['POST'])
def route_message_sendlater():

    '''
    Flask route to call the message_sendlater function.
    '''

    payload = request.get_json()
=======
    channel_id = int(payload['channel_id'])
    channel_info = helpers.get_channel(channel_id)
>>>>>>> iteration2

    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
<<<<<<< HEAD
    time_sent = int(payload['time_sent'])

    return dumps(message_sendlater(token, channel_id, message, time_sent))

@MESSAGE.route("/react", methods=['POST'])
def route_message_react():

    '''
    Flask route to call the message_react function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])
    react_id = int(payload['react_id'])

    return dumps(message_react(token, message_id, react_id))

@MESSAGE.route("/unreact", methods=['POST'])
def route_message_unreact():

    '''
    Flask route to call the message_unreact function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])
    react_id = int(payload['react_id'])

    return dumps(message_unreact(token, message_id, react_id))

@MESSAGE.route("/pin", methods=['POST'])
def route_message_pin():

    '''
    Flask route to call the message_pin function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])

    return dumps(message_pin(token, message_id))

@MESSAGE.route("/unpin", methods=['POST'])
def route_message_unpin():

    '''
    Flask route to call the message_unpin function.
    '''

    payload = request.get_json()

    token = payload['token']
    message_id = int(payload['message_id'])

    return dumps(message_unpin(token, message_id))

# ======================================================================
# =================== FUNCTION IMPLEMENTATION ==========================
# ======================================================================

def message_send(token, channel_id, message):

    '''
    Function that will take in a message as a string
    and append this message to a channel's list of messages.
    '''

    token_info = decode_token(token)
    user_id = int(token_info['u_id'])

    channel_info = helpers.get_channel(channel_id)
=======
>>>>>>> iteration2

    time_now = helpers.utc_now()

    if channel_info is None:
        raise InputError(
            description='Channel does not exist.')

    if len(message) > 1000:
        raise InputError(
            description='Message is greater than 1,000 characters')

    if len(message) == 0:
        raise InputError(
            description='Message needs to be at least 1 characters')

    if user_id not in channel_info['all_members']:
        raise AccessError(
            description='User does not have Access to send messages in the current channel')

<<<<<<< HEAD
    message_id = helpers.generate_message_id()
=======
    message_id = generate_message_id()
>>>>>>> iteration2

    message_info = {
        'message_id': message_id,
        'u_id': user_id,
        'message': message,
        'time_created': time_now,
        'reacts': [],
        'is_pinned': False
    }

    helpers.message_send_message(message_info, channel_id)

    return {
        'message_id': message_id
    }

def message_remove(token, message_id):

    '''
    Function that will take in a message ID and remove this
    message from the list of messages in a specific channel.
    '''

    token_info = decode_token(token)
    user_id = int(token_info['u_id'])

    message_channel_info = helpers.get_channel_message(message_id)

    if message_channel_info is not None:
        message_info = message_channel_info['message']
        channel_info = message_channel_info['channel']
    else:
        raise InputError(
            description='Message does not exist')

    channel_id = channel_info['channel_id']

    if message_info['u_id'] != user_id and not helpers.is_user_admin(user_id, channel_id):
        raise AccessError(
            description='User does not have access to remove this message')

    helpers.message_remove_message(message_info, channel_id)

    return {}

def message_edit(token, message_id, message):

    '''
    Function that will take in a new message that will overwrite
    an existing message in a desired channel.
    '''

    token_info = decode_token(token)
    user_id = int(token_info['u_id'])

    message_channel_info = helpers.get_channel_message(message_id)

    if message_channel_info is not None:
        message_info = message_channel_info['message']
        channel_info = message_channel_info['channel']
    else:
        raise InputError(
            description='Message does not exist')

    channel_id = channel_info['channel_id']

    if len(message) > 1000:
        raise InputError(
            description='Message is over 1,000 characters')

    if message_info['u_id'] != user_id and not helpers.is_user_admin(user_id, channel_id):
        raise AccessError(
            description='User does not have access to remove this message')

    if len(message) == 0:
        helpers.message_remove_message(message_info, channel_id)
    else:
        helpers.message_edit_message(message, message_id, channel_id)

    return {}

def message_sendlater(token, channel_id, message, time_sent):

    '''
    Function that will send a message in a desired channel at a specified
    time in the future.
    '''

    token_info = decode_token(token)
    user_id = int(token_info['u_id'])

    channel_info = helpers.get_channel(channel_id)

    if channel_info is not None:
        channel_id = channel_info['channel_id']
    else:
        raise InputError(
            description='Channel does not exist')

    if len(message) > 1000:
        raise InputError(
            description='Message is greater than 1,000 characters')

    time_now = helpers.utc_now()

    if time_now > time_sent:
        raise InputError(
            description='Time to send is in the past')

    if user_id not in channel_info['all_members']:
        raise AccessError(
            description='User does not have Access to send messages in the current channel')

<<<<<<< HEAD
    message_info = helpers.send_later(token, channel_id, message, time_sent)

    return message_info

def message_react(token, message_id, react_id):
=======
    send_later(time_sent)

    return dumps({
        'message_id': message_id
    })

def send_later(time_sent):
    time_now = helpers.utc_now()

    duration = time_sent - time_now

    timer = threading.Timer(duration, message_send)
    timer.start() 

@MESSAGE.route("/react", methods=['POST'])
def message_react():
>>>>>>> iteration2

    '''
    Function that will add a reaction to a specific message in a desired
    channel.
    '''

    token_info = decode_token(token)
    user_id = int(token_info['u_id'])

    message_channel_info = helpers.get_channel_message(message_id)

    if message_channel_info is not None:
        message_info = message_channel_info['message']
        channel_info = message_channel_info['channel']
    else:
        raise InputError(
            description='Message does not exist')

    channel_id = channel_info['channel_id']

    if helpers.is_channel_member(user_id, channel_id):
        if message_info is None:
            raise InputError(
                description='Message does not exist')

    if react_id not in data_store['reactions'].values():
        raise InputError(
            description='Reaction type is invalid')

    if helpers.has_user_reacted(user_id, message_id, channel_id, react_id):
        raise InputError(
            description='User has already reacted to this message')

    react_info = helpers.get_react(message_id, channel_id, react_id)

    if react_info is None:
        # If there are no reacts with react_id present yet.
        u_ids_reacted = [user_id]
        react_addition = {
            'react_id': react_id,
            'u_ids': u_ids_reacted
        }
        helpers.message_add_react(react_addition, message_id, channel_id)
    else:
        # If another user has already reacted with react_id.
        helpers.message_add_react_uid(user_id, message_id, channel_id, react_id)

    return {}

def message_unreact(token, message_id, react_id):

    '''
    Function that will remove a specific reaction from a message in a desired channel.
    '''

    token_info = decode_token(token)
    user_id = int(token_info['u_id'])

    message_channel_info = helpers.get_channel_message(message_id)

    if message_channel_info is not None:
        message_info = message_channel_info['message']
        channel_info = message_channel_info['channel']
    else:
        raise InputError(
            description='Message does not exist')

    channel_id = channel_info['channel_id']

    if helpers.is_channel_member(user_id, channel_id):
        if message_info is None:
            raise InputError(
                description='Message does not exist')

    if react_id not in data_store['reactions'].values():
        raise InputError(
            description='react_id is invalid')

    if helpers.get_react(message_id, channel_id, react_id) is None:
        raise InputError(
            description='Message does not have this type of reaction')

    react_removal = helpers.get_react(message_id, channel_id, react_id)

    if user_id not in react_removal['u_ids']:
        raise InputError(
            description='User has not reacted to this message')

    if len(react_removal) == 1:
        # If the current user is the only reaction on the message.
        helpers.message_remove_reaction(react_removal, message_id, channel_id)
    else:
        # If there are other u_ids reacting with the same react ID.
        helpers.message_remove_react_uid(user_id, message_id, channel_id, react_id)

    return {}

def message_pin(token, message_id):

    '''
    Function that will mark a message as 'pinned' to be given special
    display treatment by the frontend.
    '''

    token_info = decode_token(token)
    user_id = int(token_info['u_id'])

    message_channel_info = helpers.get_channel_message(message_id)

    if message_channel_info is not None:
        channel_info = message_channel_info['channel']
    else:
        raise InputError(
            description='Message does not exist')

    channel_id = channel_info['channel_id']

    if not helpers.is_user_admin(user_id, channel_id):
        raise InputError(
            description='User is not an admin')

    if helpers.is_pinned(message_id, channel_id):
        raise InputError(
            description='Message is already pinned')

    if not helpers.is_channel_member(user_id, channel_id):
        raise AccessError(
            description='User is not a member of the channel')

    helpers.message_pin(message_id, channel_id)

    return {}

def message_unpin(token, message_id):

    '''
    Function that will remove the 'pinned' status of a message.
    '''

    token_info = decode_token(token)
    user_id = int(token_info['u_id'])

    message_channel_info = helpers.get_channel_message(message_id)

    if message_channel_info is not None:
        channel_info = message_channel_info['channel']
    else:
        raise InputError(
            description='Message does not exist')

    channel_id = channel_info['channel_id']

    if not helpers.is_user_admin(user_id, channel_id):
        raise InputError(
            description='User is not an admin')

    if not helpers.is_pinned(message_id, channel_id):
        raise InputError(
            description='Message is not pinned')

    if not helpers.is_channel_member(user_id, channel_id):
        raise AccessError(
            description='User is not a member of the channel')

    helpers.message_unpin(message_id, channel_id)

    return {}

if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
