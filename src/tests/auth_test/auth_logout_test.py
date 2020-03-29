''' System tests for auth_logout'''
import pytest
import auth
from error import AccessError, InputError


def test_logout(reset, test_user):  # pylint: disable=W0613
    '''Test that auth_logout returns True on successful Logout'''

    assert auth.auth_logout(test_user['token'])['is_success']


def test_logout_invalid_token(reset, invalid_token):  # pylint: disable=W0613
    '''Test that auth_logout raises an AccessError when given invalid token'''

    with pytest.raises(AccessError):
        auth.auth_logout(invalid_token)


def test_logout_insufficient_params(reset):  # pylint: disable=W0613
    '''Test input of invalid parameters into auth_logout'''

    with pytest.raises(InputError):
        auth.auth_logout(None)
