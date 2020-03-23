import sys
import jwt
import math
import hashlib
from json import dumps
from flask import Flask, request, Blueprint
from flask_cors import CORS
from error import AccessError, InputError
from email_validation import invalid_email
from datetime import datetime, timedelta, timezone
from data_store import data_store, SECRET
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

    channel_info = get_channel(channel_id)
    if not channel_info['messages']:
        messageID = 1
    else:
        messageIDs = [message['message_id'] for message in channel_info['messages']]
        messageID = max(messageIDs) + 1

@MESSAGE.route("/send", methods=['POST'])
def message_send():

    '''
    Function that will send a message to a desired channel.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    message = payload['message']
    message_id = generate_message_id(channel_id)

    time_now = helpers.utc_now()

    channel_id = payload['channel_id']
    channel_info = helpers.get_channel(channel_id)

    if len(message) > 1000:
        raise InputError(
            description='Message is greater than 1,000 characters')

    if len(message) == 0:
        raise InputError(
            description='Message needs to be at least 1 characters')

    if user_id not in channel_info['all_members']:
        raise AccessError(
            description='User does not have Access to send messages in the current channel')

    message = {
        'message_id': message_id,
        'u_id': user_id,
        'message': message,
        'time_created': time_now,
        'reacts': [],
        'is_pinned': False
    }

    channel_info['messages'].append(message)

    return dumps({
        'message_id': message_id
    })

@MESSAGE.route("/remove", methods=['DELETE'])
def message_remove():

    '''
    Function that will remove a message from a desired channel.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    message_id = payload['message_id']

    channel_id = payload['channel_id']
    channel_info = helpers.get_channel(channel_id)

    message_info = helpers.get_message(message_id)

    if not helpers.message_existance(message_id):
        raise InputError(
            description='Message does not exist')

    if message_info['u_id'] != user_id and not helpers.is_user_admin(user_id, channel_id):
        raise AccessError(
            description='User does not have access to remove this message')

    channel_info['messages'].remove(message_info)

    return dumps({})

@MESSAGE.route("/edit", methods=['PUT'])
def message_edit():

    '''
    Function that will edit an existing message within a desired channel.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    message_id = payload['message_id']
    new_message = payload['message']

    channel_id = payload['channel_id']
    channel_info = helpers.get_channel(channel_id)

    message_info = helpers.get_message(message_id)

    if len(new_message) > 1000:
        raise InputError(
            description='Message is over 1,000 characters')

    if message_info['u_id'] != user_id and not helpers.is_user_admin(user_id, channel_id):
        raise AccessError(
            description='User does not have access to remove this message')

    if len(new_message) == 0:
        channel_info['messages'].remove(message_info)
    else:
        message_info['message'] = new_message

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

    message = payload['message']
    message_id = generate_message_id(channel_id)

    channel_id = payload['channel_id']
    channel_info = helpers.get_channel(channel_id)

    if helpers.get_channel(channel_id) == None:
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

    message_id = payload['message_id']
    message_info = helpers.get_message(message_id)

    react_id = payload['react_id']

    channel_id = payload['channel_id']
    channel_info = helpers.get_channel(channel_id)

    if not helpers.check_message_channel_permissions(message_id, channel_id, u_id):
        raise InputError(
            description='Message ID does not exist')

    if react_id not in data_store['reactions'].values():
        raise InputError(
            description='react_id is invalid')

    if helpers.has_user_reacted(user_id, message_id, channel_id, react_id):
        raise InputError(
            description='User has already reacted to this message')

    react_info = helpers.get_react(message_id, channel_id, react_id)

    if react_info == None:
        # If there is no react with react_id present yet.
        u_ids_reacted = [user_id]
        react_addition = {
            'react_id': react_id,
            'u_ids': u_ids_reacted
        }
        message_info['reacts'].append(react_info)
    else:
        # If another user has already reacted with react_id
        u_ids_already_reacted = react_info['u_ids']
        u_ids_already_reacted.append(user_id)

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
    channel_info = helpers.get_channel(channel_id)

    message_id = payload['message_id']
    message_info = helpers.get_message(message_id, channel_id)

    react_id = payload['react_id']

    if not helpers.check_message_channel_permissions(message_id, channel_id, user_id):
        raise InputError(
            description='Message ID is invalid')
    
    if react_id not in data_store['reactions'].values():
        raise InputError(
            description='react_id is invalid')
    
    if helpers.get_react(message_id, channel_id, react_id) == None:
        raise InputError(
            description='Message does not have this type of reaction')

    react_removal = helpers.get_react(message_id, channel_id, react_id)

    if user_id not in react_removal['u_ids']:
        raise InputError(
            description='User has not reacted to this message')
    
    if len(react_removal) == 1:
        message_info['reacts'].remove(react_removal)
    else:
        react_removal['u_ids'].remove(user_id)
    
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
    channel_info = helpers.get_channel(channel_id)

    message_id = payload['message_id']
    message_info = helpers.get_message(message_id, channel_id)

    if message_info == None:
        raise InputError(
            description='message_id is not a valid message')
    
    if not helpers.is_user_admin(user_id, channel_id):
        raise InputError(
            description='User is not an admin')
    
    if helpers.is_pinned(message_id, channel_id):
        raise InputError(
            description='Message is already pinned')
    
    if not helpers.is_channel_member(user_id, channel_id):
        raise AccessError(
            description='User is not a member of the channel')
    
    message_info['is_pinned'] = 1

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
    channel_info = helpers.get_channel(channel_id)

    message_id = payload['message_id']
    message_info = helpers.get_message(message_id, channel_id)

    if message_info == None:
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

    message_info['is_pinned'] = 0

    return dumps({})

if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
