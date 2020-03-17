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

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

@APP.route("/send", methods=['POST'])
def message_send(token, channel_id, message):
    token = request.args.get('token')
    channelid = request.args.get('channel_id')
    message = request.args.get('message')

    if (len(message) > 1000):
        raise InputError(
            description='Message is greater than 1,000 characters')
    
    for channels in data_store['channels']:
        if channelid == channels['channel_id']:
            if 


    AccessError when:  the authorised user has not joined the channel they are trying to post to

    message_id = 

    message = {
        'message_id':
        'u_id':
        'message':
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
