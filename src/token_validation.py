import jwt
from error import AccessError
from data_store import data_store, SECRET
from helpers import get_all_u_id


def decode_token(token):
    '''Decode a given jwt token and return the payload'''

    if token in data_store['token_blacklist']:
        raise AccessError(description='Token is invalid')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except jwt.ExpiredSignatureError:
        raise AccessError(description='Session has expired')
    except:
        raise AccessError(description='Token is invalid')

    if payload['u_id'] not in get_all_u_id():
        raise AccessError(description='u_id does not belong to a user')

    return payload