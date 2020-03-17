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

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

message = Blueprint('message', __name__)

def utc_now():
    return int(datetime.now(timezone.utc).timestamp())

def get_channel(channel_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            return channel
    return None

def generate_message_id(channel_id):
    channel_info = get_channel(channel_id)
    if not channel_info['messages']:
        messageID = 1
    else:
        messageIDs = [message['message_id'] for message in channel_info['messages']]
        messageID = max(messageIDs) + 1 

@message.route("/send", methods=['POST'])
def message_send():
    channelid = request.args.get('channel_id')
    channel_info = get_channel(channelid)
    messageID = generate_message_id(channelid)

    token = request.args.get('token')
    payload = decode_token(token)
    userID = payload['u_id']

    message = request.args.get('message')
    time_now = utc_now()

    if (len(message) > 1000):
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

def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    return {
    }

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
    print('hello?')
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
