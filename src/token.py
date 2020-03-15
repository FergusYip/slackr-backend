import jwt
from error import AccessError
from data_store import data_store, SECRET

def decode_token(token):
    '''Decide a given jwt token and return the payload'''
    
    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Token is invalid')

    if token not in data_store['tokens']:
        raise AccessError(description='Token is invalid')

    return payload