from json import dumps
from flask import request, Blueprint
from error import InputError
from data_store import data_store
from token_validation import decode_token

CHANNELS = Blueprint('channels', __name__)


@CHANNELS.route("/list", methods=['GET'])
def route_channels_list():
    token = request.values.get('token')
    return dumps(channels_list(token))


@CHANNELS.route("/listall", methods=['GET'])
def route_channels_listall():
    token = request.values.get('token')
    return dumps(channels_listall(token))


@CHANNELS.route("/create", methods=['POST'])
def route_channels_create():
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']
    return dumps(channels_create(token, name, is_public))


def channels_list(token):
    token_payload = decode_token(token)
    u_id = token_payload['u_id']
    channels = []
    for channel in data_store['channels']:
        if u_id in channel['all_members']:
            channel_dict = {
                'channel_id': channel['channel_id'],
                'name': channel['name']
            }
            channels.append(channel_dict)

    return {'channels': channels}


def channels_listall(token):
    decode_token(token)

    channels = []
    for channel in data_store['channels']:
        channel_dict = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        channels.append(channel_dict)

    return {'channels': channels}


def channels_create(token, name, is_public):
    token_payload = decode_token(token)

    if invalid_channel_name(name):
        raise InputError(description='Name is more than 20 characters long')

    channel_id = generate_channel_id()

    u_id = token_payload['u_id']

    # Assuming that the user creating the channel automatically joins the channel
    channel = {
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [u_id],
        'all_members': [u_id],
        'messages': [],
        'standup': {
            'is_active': False,
            'starting_user': None,
            'time_finish': None,
            'messages': []
        }
    }

    data_store['channels'].append(channel)
    return {'channel_id': channel_id}


def invalid_channel_name(channel_name):
    return len(channel_name) > 20


def generate_channel_id():
    data_store['max_ids']['channel_id'] += 1
    return data_store['max_ids']['channel_id']


if __name__ == "__main__":
    pass
