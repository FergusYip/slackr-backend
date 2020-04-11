'''
Implementation of channels routes for slackr app
'''
from error import InputError
from data_store import DATA_STORE as data_store
from token_validation import decode_token
from helpers import generate_id


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
    """ Provide a list of all channels

        Parameters:
                token (str): JWT

        Returns (dict):
                channels (list): List of channels

        """

    if token is None:
        raise InputError(description='Insufficient parameters')

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

    if invalid_channel_name(name):
        raise InputError(description='Name is more than 20 characters long')

    channel_id = generate_id('channel_id')

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
        },
        'hangman': {
            'is_active': False,
            'word': None,
            'guesses': [],
            'correct': [],
            'stage': 0
        }
    }

    data_store['channels'].append(channel)
    return {'channel_id': channel_id}


def invalid_channel_name(channel_name):
    """ Checks if a channel name is invalid

        Parameters:
                channel_name (str): Channel name

        Returns:
                (bool): Whether the channel name is invalid

        """
    return len(channel_name) > 20


if __name__ == "__main__":
    pass
