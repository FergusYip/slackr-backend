import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_logout(reset, new_user):
    '''Test that auth_logout returns True on successful Logout'''

    user = new_user()
    logout_input = {'token': user['token']}
    logout = requests.post(f"{BASE_URL}/auth/logout", json=logout_input).json()
    assert logout['is_success']


def test_logout_invalid_token(reset, invalid_token):
    '''Test that auth_logout raises an AccessError when given invalid token'''

    logout_input = {'token': invalid_token}
    error = requests.post(f"{BASE_URL}/auth/logout", json=logout_input)
    with pytest.raises(requests.HTTPError):
        requests.Response.raise_for_status(error)
