'''Module to encode and decode JWT'''
from datetime import datetime, timedelta
import jwt
from error import AccessError
from data_store import DATA_STORE

SECRET = 'the chunts'


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
        'exp': datetime.utcnow() + timedelta(minutes=30)
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

    if token in DATA_STORE.token_blacklist:
        raise AccessError(description='Token is invalid')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise AccessError(description='Session has expired')
    except:
        raise AccessError(description='Token is invalid')

    if payload['iat'] < DATA_STORE.time_created:
        raise AccessError(description='Session has expired')

    u_id = payload['u_id']
    hangman_bot_u_id = DATA_STORE.preset_profiles['hangman_bot'].u_id

    if u_id not in DATA_STORE.u_ids and u_id != hangman_bot_u_id:
        raise AccessError(description='u_id does not belong to a user')

    return payload
