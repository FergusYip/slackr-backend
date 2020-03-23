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
import helpers

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

MESSAGE = Blueprint('message', __name__)

def generate_message_id(channel_id):

    '''
    Function that will generate a unique message_id within a specific channel.
    '''

    channel_info = helpers.get_channel(channel_id)
    if not channel_info['messages']:
        message_id = 1
    else:
        message_ids = [message['message_id'] for message in channel_info['messages']]
        message_id = max(message_ids) + 1
    return message_id

@MESSAGE.route("/send", methods=['POST'])
def message_send():

    '''
    Function that will take in a string as a message
    and append this message to a channel's list of messages.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    channel_id = payload['channel_id']
    channel_info = helpers.get_channel(channel_id)

    message = payload['message']
    message_id = generate_message_id(channel_id)

    time_now = helpers.utc_now()

    if len(message) > 1000:
        raise InputError(
            description='Message is greater than 1,000 characters')

    if len(message) == 0:
        raise InputError(
            description='Message needs to be at least 1 characters')

    if user_id not in channel_info['all_members']:
        raise AccessError(
            description='User does not have Access to send messages in the current channel')

    message_info = {
        'message_id': message_id,
        'u_id': user_id,
        'message': message,
        'time_created': time_now,
        'reacts': [],
        'is_pinned': False
    }

    helpers.message_send_message(message_info, channel_id)

    return dumps({
        'message_id': message_id
    })

@MESSAGE.route("/remove", methods=['DELETE'])
def message_remove():

    '''
    Function that will take in a message ID and remove this
    message from the list of messages in a specific channel.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    message_id = payload['message_id']
    channel_id = payload['channel_id']

    message_info = helpers.get_message(message_id, channel_id)

    if helpers.get_message(message_id, channel_id) is None:
        raise InputError(
            description='Message does not exist')

    if message_info['u_id'] != user_id and not helpers.is_user_admin(user_id, channel_id):
        raise AccessError(
            description='User does not have access to remove this message')

    helpers.message_remove_message(message_info, channel_id)

    return dumps({})

@MESSAGE.route("/edit", methods=['PUT'])
def message_edit():

    '''
    Function that will take in a new message that will overwrite
    an existing message in a desired channel.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    message_id = payload['message_id']
    new_message = payload['message']

    channel_id = payload['channel_id']

    message_info = helpers.get_message(message_id, channel_id)

    if len(new_message) > 1000:
        raise InputError(
            description='Message is over 1,000 characters')

    if message_info['u_id'] != user_id and not helpers.is_user_admin(user_id, channel_id):
        raise AccessError(
            description='User does not have access to remove this message')

    if len(new_message) == 0:
        helpers.message_remove_message(message_info, channel_id)
    else:
        helpers.message_edit_message(new_message, message_id, channel_id)

    return dumps({})

@MESSAGE.route("/sendlater", methods=['POST'])
def message_sendlater():

    '''
    CURRENTLY UNFINISHED!!!
    Function that will send a message in a desired channel at a specified
    time in the future.
    CURRENTLY UNFINISHED!!!
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    time_sent = payload['time_sent']

    channel_id = payload['channel_id']
    channel_info = helpers.get_channel(channel_id)

    message = payload['message']
    message_id = generate_message_id(channel_id)

    if helpers.get_channel(channel_id) is None:
        raise InputError(
            description='Channel ID is invalid')

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

    return dumps({
        'message_id': message_id
    })

@MESSAGE.route("/react", methods=['POST'])
def message_react():

    '''
    Function that will add a reaction to a specific message in a desired
    channel.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    channel_id = payload['channel_id']

    message_id = payload['message_id']

    react_id = payload['react_id']

    if helpers.is_channel_member(user_id, channel_id):
        if helpers.get_message(message_id, channel_id) is None:
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

    return dumps({})

@MESSAGE.route("/unreact", methods=['POST'])
def message_unreact():

    '''
    Function that will remove a specific reaction from a message in a desired channel.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    channel_id = payload['channel_id']

    message_id = payload['message_id']

    react_id = payload['react_id']

    if helpers.is_channel_member(user_id, channel_id):
        if helpers.get_message(message_id, channel_id) is None:
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

    return dumps({})

@MESSAGE.route("/pin", methods=['POST'])
def message_pin():

    '''
    Function that will mark a message as 'pinned' to be given special
    display treatment by the frontend.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    channel_id = payload['channel_id']

    message_id = payload['message_id']
    message_info = helpers.get_message(message_id, channel_id)

    if message_info is None:
        raise InputError(
            description='Message is invalid')

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

    return dumps({})

@MESSAGE.route("/unpin", methods=['POST'])
def message_unpin(token, message_id):

    '''
    Function that will remove the 'pinned' status of a message.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    channel_id = payload['channel_id']

    message_id = payload['message_id']
    message_info = helpers.get_message(message_id, channel_id)

    if message_info is None:
        raise InputError(
            description='message_id is not a valid message')

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

    return dumps({})

if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
