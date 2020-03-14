import sys
import jwt
import math
import hashlib
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import AccessError, InputError
from email_validation import invalid_email

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

SECRET = 'the chunts'

data_store = {'users': [], 'channels': [], 'tokens': []}


def invalid_channel_name(channel_name):
    return len(channel_name) > 20


@APP.route("/channels/list", methods=['GET'])
def channels_list():
    token = request.args.get('token')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Token is invalid')

    u_id = payload['u_id']

    channels = []
    for channel in data_store['channels']:
        if u_id in channel['all_members']:
            channel_dict = {
                'channel_id': channel['channel_id'],
                'name': channel['name']
            }
            channels.append(channel_dict)

    return dumps({'channels': channels})


@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    token = request.args.get('token')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Token is invalid')

    channels = []
    for channel in data_store['channels']:
        channel_dict = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        channels.append(channel_dict)

    return dumps({'channels': channels})


@APP.route("/channels/create", methods=['POST'])
def channels_create():
    token = request.args.get('token')
    name = request.args.get('name')
    is_public = request.args.get('is_public')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(
            description='Unable to create channel due to invalid token')

    if invalid_channel_name(name):
        raise InputError(description='Name is more than 20 characters long')

    if not data_store['channels']:
        channel_id = 1
    else:
        channel_id = max(data_store['channels']['channel_id']) + 1

    u_id = payload['u_id']

    # Assuming that the user creating the channel automatically joins the channel
    channel = {
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [u_id],
        'all_members': [u_id],
        'messages': []
    }

    data_store['channels'].append(channel)

    return dumps({'channel_id': channel_id})


if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
