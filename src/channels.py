'''
Implementation of channels routes for slackr app
'''
from error import InputError
from data_store import data_store, Channel
from token_validation import decode_token


def channels_list(token):
    """ Provide a list of all channels that the authorised user is part of

	Parameters:
		token (str): JWT

	Returns (dict):
		channels (list): List of channels

	"""
    if token is None:
        raise InputError(description='Insufficient parameters')

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

    if token is None:
        raise InputError(description='Insufficient parameters')

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

    if None in {token, name, is_public}:
        raise InputError(description='Insufficient parameters')

    token_payload = decode_token(token)

    if len(name) > 20:
        raise InputError(description='Name is more than 20 characters long')

    user = data_store.get_user(token_payload['u_id'])
    channel = Channel(user, name, is_public)
    data_store.add_channel(channel)
    user.add_channel(channel)
    return {'channel_id': channel.channel_id}


if __name__ == "__main__":
    pass
