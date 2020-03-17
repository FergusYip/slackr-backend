import jwt
from error import AccessError
from data_store import data_store, SECRET


def decode_token(token):
    '''Decode a given jwt token and return the payload'''

    if token in data_store['token_blacklist']:
        raise AccessError(description='Token is invalid')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Token is invalid')

    return payload