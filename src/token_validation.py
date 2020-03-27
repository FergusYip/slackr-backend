from datetime import datetime, timedelta
import jwt
from error import AccessError
from data_store import data_store, SECRET


def encode_token(u_id):
    payload = {
        'u_id': u_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')
    return token


def decode_token(token):
    '''Decode a given jwt token and return the payload'''

    if token in data_store.token_blacklist:
        raise AccessError(description='Token is invalid')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except jwt.ExpiredSignatureError:
        raise AccessError(description='Session has expired')
    except:
        raise AccessError(description='Token is invalid')

    if payload['iat'] < int(data_store.time_created):
        raise AccessError(description='Session has expired')

    if payload['u_id'] not in data_store.u_ids:
        raise AccessError(description='u_id does not belong to a user')

    return payload
