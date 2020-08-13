'''
Functions to encode, decode, and validate JWT tokens.
'''

from datetime import datetime

import jwt

from slackr.error import AccessError
from slackr.models.expired_token import ExpiredToken
from slackr.models.user import User
from slackr.utils.constants import SECRET


def encode_token(u_id):
    ''' Encodes a JWT token with user ID, current time, and expiry time

	Parameters:
		u_id (int): ID of user

	Returns (dict):
		token (str): JWT

	'''
    payload = {
        'u_id': u_id,
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')
    return token


def decode_token(token):
    ''' Decode a given jwt token

	Parameters:
		u_id (int): ID of user

	Returns (dict):
		payload (dict): JWT

	'''

    if ExpiredToken.query.filter_by(token=token).first() is not None:
        raise AccessError(description='Token is invalid')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET, algorithms='HS256')
    except:
        raise AccessError(description='Token is invalid')

    # if payload['iat'] < DATA_STORE.time_created:
    #     raise AccessError(description='Session has expired')

    u_id = payload['u_id']
    # hangman_bot_u_id = DATA_STORE.preset_profiles['hangman_bot'].u_id

    if User.query.filter_by(u_id=u_id).first() is None:
        # if u_id not in DATA_STORE.u_ids and u_id != hangman_bot_u_id:
        raise AccessError(description='u_id does not belong to a user')

    return payload
