import requests
import pytest
from error import AccessError

BASE_URL = 'http://127.0.0.1:8080'


def test_logout(reset, new_user):
    '''Test that auth_logout returns True on successful Logout'''

    user = new_user()

    logout = requests.post(f"{BASE_URL}/auth/logout",
                           json={
                               'token': user['token']
                           }).json()
    assert logout['is_success']


def test_logout_invalid_token(reset, invalid_token):
    '''Test that auth_logout raises an AccessError when given invalid token'''

    with pytest.raises(AccessError):
        requests.post(f"{BASE_URL}/auth/logout", json={'token': invalid_token})
