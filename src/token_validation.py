'''Module to encode and decode JWT'''
from datetime import datetime, timedelta
import jwt
from error import AccessError
from data_store import data_store
from helpers import get_all_u_id

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

    if token in data_store['token_blacklist']:
        raise AccessError(description='Token is invalid')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise AccessError(description='Session has expired')
    except:
        raise AccessError(description='Token is invalid')

    if payload['iat'] < data_store['time_created']:
        raise AccessError(description='Token no longer valid')

    if payload['u_id'] not in get_all_u_id():
        raise AccessError(description='u_id does not belong to a user')

    return payload
