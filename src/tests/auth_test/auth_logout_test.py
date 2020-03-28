''' System tests for auth_logout'''
import pytest
import auth
from error import InputError, AccessError


def test_logout(reset, test_user):
    '''Test that auth_logout returns True on successful Logout'''

    assert auth.auth_logout(test_user['token'])['is_success']


def test_logout_invalid_token(reset, invalid_token):
    '''Test that auth_logout raises an AccessError when given invalid token'''

    with pytest.raises(AccessError):
        auth.auth_logout(invalid_token)['is_success']
