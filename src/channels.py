import sys
from json import dumps
from flask import Flask, request, Blueprint
from flask_cors import CORS
from error import AccessError, InputError
from data_store import data_store
from token_validation import decode_token

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

CHANNELS = Blueprint('channels', __name__)


def invalid_channel_name(channel_name):
    return len(channel_name) > 20


@CHANNELS.route("/list", methods=['GET'])
def channels_list():
    payload = request.get_json()
    token = payload['token']

    decode_token(token)

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


@CHANNELS.route("/listall", methods=['GET'])
def channels_listall():
    payload = request.get_json()
    token = payload['token']

    decode_token(token)

    channels = []
    for channel in data_store['channels']:
        channel_dict = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        channels.append(channel_dict)

    return dumps({'channels': channels})


@CHANNELS.route("/create", methods=['POST'])
def channels_create():
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']

    token_payload = decode_token(token)

    if invalid_channel_name(name):
        raise InputError(description='Name is more than 20 characters long')

    if not data_store['channels']:
        channel_id = 1
    else:
        channel_ids = [
            channel['channel_id'] for channel in data_store['channels']
        ]
        channel_id = max(channel_ids) + 1

    u_id = token_payload['u_id']

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
