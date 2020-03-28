'''Pytest script for testing /auth/logout route'''
import requests as req
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_logout(reset, new_user):  # pylint: disable=W0613
    '''Test that auth_logout returns True on successful Logout'''

    user = new_user()
    logout_input = {'token': user['token']}
    logout = req.post(f"{BASE_URL}/auth/logout", json=logout_input).json()
    assert logout['is_success']


def test_logout_invalid_token(reset, invalid_token):  # pylint: disable=W0613
    '''Test that auth_logout raises an AccessError when given invalid token'''

    logout_input = {'token': invalid_token}
    with pytest.raises(req.HTTPError):
        req.post(f"{BASE_URL}/auth/logout",
                 json=logout_input).raise_for_status()
