'''
Implementation of channels routes for slackr app
'''
from json import dumps
from flask import request, Blueprint
from error import InputError
from data_store import data_store, Channel
from token_validation import decode_token

CHANNELS = Blueprint('channels', __name__)


@CHANNELS.route("/channels/list", methods=['GET'])
def route_channels_list():
    '''Flask route for /channels/list'''
    token = request.values.get('token')
    return dumps(channels_list(token))


@CHANNELS.route("/channels/listall", methods=['GET'])
def route_channels_listall():
    '''Flask route for /channels/listall'''
    token = request.values.get('token')
    return dumps(channels_listall(token))


@CHANNELS.route("/channels/create", methods=['POST'])
def route_channels_create():
    '''Flask route for /channels/create'''
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']
    return dumps(channels_create(token, name, is_public))


def channels_list(token):
    """ Provide a list of all channels that the authorised user is part of

	Parameters:
		token (str): JWT

	Returns (dict):
		channels (list): List of channels

	"""
    token_payload = decode_token(token)
    user = data_store.get_user(token_payload['u_id'])
    channels = [channel.id_name for channel in user.channels]
    return {'channels': channels}


def channels_listall(token):
    """ Provide a list of all channels

	Parameters:
		token (str): JWT

	Returns (dict):
		channels (list): List of channels

	"""
    decode_token(token)
    channels = [channel.id_name for channel in data_store.channels]
    return {'channels': channels}


def channels_create(token, name, is_public):
    """ Creates a new public or private channel called name

	Parameters:
		token (str): JWT
		name (str): Desired name of channel
		is_public (bool): Whether the channel is public

	Returns (dict):
		channel_id  (int): Channel ID

	"""
    token_payload = decode_token(token)

    if len(name) > 20:
        raise InputError(description='Name is more than 20 characters long')

    user = data_store.get_user(token_payload['u_id'])
    channel = Channel(user, name, is_public)
    data_store.add_channel(channel)
    return {'channel_id': channel.channel_id}


if __name__ == "__main__":
    pass
