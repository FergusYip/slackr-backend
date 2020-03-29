'''System tests for token_validation'''
from datetime import datetime, timedelta
from time import sleep
import pytest
import jwt
from auth import auth_logout
from error import AccessError
from token_validation import decode_token, SECRET
from workspace import workspace_reset


def test_expired_token(reset, new_user):
    '''Test that an expired token raises an AccessError'''
    user = new_user()
    payload = {
        'u_id': user['u_id'],
        'iat': datetime.utcnow() + timedelta(minutes=-60),
        'exp': datetime.utcnow() + timedelta(minutes=-30)
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')

    with pytest.raises(AccessError):
        decode_token(token)


def test_modified_token(reset, new_user):
    '''Test that an modified token raises an AccessError'''
    user = new_user()
    payload = {
        'u_id': user['u_id'],
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, 'Wrong secret',
                       algorithm='HS256').decode('utf-8')

    with pytest.raises(AccessError):
        decode_token(token)


def test_invalidated_token(reset, new_user):
    '''Test that an invalidated token raises an AccessError'''
    user = new_user()
    token = user['token']
    auth_logout(user['token'])
    with pytest.raises(AccessError):
        decode_token(token)


def test_reset_token(reset, new_user):
    '''Test that an token is no longer valid after a reset raises an AccessError'''
    user = new_user()
    token = user['token']
    workspace_reset()
    sleep(1)
    with pytest.raises(AccessError):
        decode_token(token)


def test_userless_token(reset, new_user):
    '''Test that an token containing a invalid u_id raises an AccessError'''
    with pytest.raises(AccessError):
        decode_token(None)