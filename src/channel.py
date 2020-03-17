import sys
import jwt
from json import dumps
from flask import Flask, request, Blueprint
from flask_cors import CORS
from error import AccessError, InputError
from data_store import data_store, SECRET
from token_validation import decode_token
# from helper import

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

channel = Blueprint('channel', __name__)


@channel.route("/invite", methods=['POST'])
def channel_invite():
    payload = request.get_json()

    token = payload['token']
    c_id = payload['channel_id']
    invited = payload['u_id']

    token_data = decode_token(token)

    if invited not in data_store['users']:
        raise InputError(description='User does not exist.')

    add_into_channel(token_data['u_id'], c_id, invited)

    return dumps({})


def add_into_channel(inviter, c_id, invited):
    '''
    Appends a user ID into the channel with ID c_id.
    '''
    for channels in data_store['channels']:
        if channels['channel_id'] == c_id:
            if inviter not in channels['all_members']:
                raise AccessError(
                    description='User does not have permission to invite')
            else:
                channels['all_members'].append(invited)


@channel.route("/details", methods=['GET'])
def channel_details(token, channel_id):
    payload = request.get_json()

    token = payload['token']
    c_id = payload['channel_id']

    token_data = decode_token(token)
    auth_user = token_data['u_id']
    channels = data_store['channels']

    if c_id not in channels:
        raise InputError

    if auth_user not in channels['all_members']:
        raise AccessError


def channel_messages(token, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }


def channel_leave(token, channel_id):
    return {
    }


def channel_join(token, channel_id):
    return {
    }


def channel_addowner(token, channel_id, u_id):
    return {
    }


def channel_removeowner(token, channel_id, u_id):
    return {
    }
