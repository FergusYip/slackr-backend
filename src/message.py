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
from data_store import data_store, SECRET, OWNER, MEMBER
from token_validation import decode_token
import helpers

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

MESSAGE = Blueprint('message', __name__)

def generate_message_id(channel_id):
    channel_info = get_channel(channel_id)
    if not channel_info['messages']:
        messageID = 1
    else:
        messageIDs = [message['message_id'] for message in channel_info['messages']]
        messageID = max(messageIDs) + 1

@MESSAGE.route("/send", methods=['POST'])
def message_send():
    channelid = request.args.get('channel_id')
    channel_info = helpers.get_channel(channelid)
    messageID = generate_message_id(channelid)

    token = request.args.get('token')
    payload = decode_token(token)
    userID = payload['u_id']

    message = request.args.get('message')
    time_now = helpers.utc_now()

    if len(message) > 1000:
        raise InputError(
            description='Message is greater than 1,000 characters')

    if userID not in channel_info['all_members']:
        raise AccessError(
            description='User does not have Access to send messages in the current channel')

    message = {
        'message_id': messageID,
        'u_id': userID,
        'message': message,
        'time_created': time_now,
        'reacts': [],
        'is_pinned': False
    }

    data_store['channels']['messages'].append(message)

    return dumps({
        'message_id': messageID
    })

@MESSAGE.route("/remove", methods=['DELETE'])
def message_remove():
    token = request.args.get('token')
    payload = decode_token(token)
    userID = payload['u_id']

    message_info = helpers.get_message(message_id)

    channelid = request.args.get('channel_id')
    channel_info = helpers.get_channel(channelid)

    if not message_existance(message_id):
        raise InputError(
            description='Message does not exist')

    if message_info['u_id'] != userID and not is_user_admin(userID, channelid):
        raise AccessError(
            description='User does not have access to remove this message')

    channel_info['messages'].remove(message_info)

    return dumps({})

@MESSAGE.route("/edit", methods=['PUT'])
def message_edit(token, message_id, message):
    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    userID = token_info['u_id']

    message_id = payload['message_id']
    new_message = payload['message']

    channelid = payload['channel_id']
    channel_info = helpers.get_channel(channelid)

    message_info = helpers.get_message(message_id)

    if len(new_message) > 1000:
        raise InputError(
            description='Message is over 1,000 characters')

    if message_info['u_id'] != userID and not is_user_admin(userID, channelid):
        raise AccessError(
            description='User does not have access to remove this message')

    if len(new_message) == 0:
        channel_info['messages'].remove(message_info)
    else: 
        message_info['message'] = new_message
    
    return dumps({})

def message_sendlater(token, channel_id, message, time_sent):
    return {
        'message_id': 1,
    }

def message_react(token, message_id, react_id):
    return {
    }

def message_unreact(token, message_id, react_id):
    return {
    }

def message_pin(token, message_id):
    return {
    }

def message_unpin(token, message_id):
    return {
    }

if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
