import sys
import jwt
import math
import hashlib
from json import dumps
from flask import Flask, request, Blueprint
from flask_cors import CORS
from error import AccessError, InputError
from email_validation import invalid_email
from datetime import datetime, timedelta
from data_store import data_store, PERMISSIONS, SECRET, OWNER, MEMBER
from token_validation import decode_token

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

@APP.route("/send", methods=['POST'])
def message_send(token, channel_id, message):
    token = request.args.get('token')
    channelid = request.args.get('channel_id')
    message = request.args.get('message')

    payload = decode_token(token)
    userID = payload['u_id']

    if (len(message) > 1000):
        raise InputError(
            description='Message is greater than 1,000 characters')
    
    for channels in data_store['channels']:
        if channelid == channels['channel_id']:
            if userID not in channels['all_members']:
                raise AccessError(
                    description='User does not have Access to send messages in the current channel')
            break

    for channels in data_store['channels']:
        if channelid == channels['channel_id']:
            if not channels['messages']:
                messageID = 1
            else:
                messageIDs = [message['message_id'] for message in channels['messages']]
                messageID = max(messageIDs) + 1 

    message = {
        'message_id': messageID
        'u_id': userID
        'message': message
        'time_created':
        'reacts':
    }

    return {
        'message_id': 1,
    }

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
