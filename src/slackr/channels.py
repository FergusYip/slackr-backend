'''
Functions to provide channel creation and lists to the program. Will allow
users to create channels and generate lists of channels.
'''

from slackr.error import InputError
from slackr.token_validation import decode_token
from slackr import db
from slackr.models import User, Channel


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
    user = User.query.get(token_payload['u_id'])
    channels = [channel.id_name for channel in user.channels]
    return {'channels': channels}


def channels_listall(token):
    """ Provide a list of all public channels

    Parameters:
            token (str): JWT

    Returns (dict):
            channels (list): List of channels
    """

    if token is None:
        raise InputError(description='Insufficient parameters')

    decode_token(token)
    public_channels = Channel.query.filter_by(is_public=True).all()
    channels = [channel.id_name for channel in public_channels]
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

    user = User.query.get(token_payload['u_id'])
    channel = Channel(user, name, is_public)

    db.session.add(channel)
    db.session.commit()

    return {'channel_id': channel.channel_id}


if __name__ == "__main__":
    pass
