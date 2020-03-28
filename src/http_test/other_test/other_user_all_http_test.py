'''Pytest script for testing users_all route'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_users_all_single_user(reset, new_user, get_user_profile):  # pylint: disable=W0613
    '''Test that a single user profile is returned by user_all'''

    user = new_user(email='user_1@email.com')
    users_all_input = {'token': user['token']}

    user_profile = get_user_profile(user['token'], user['u_id'])

    users_all = requests.get(f'{BASE_URL}/users/all',
                             params=users_all_input).json()

    assert user_profile in users_all['users']


def test_users_all_multiple_users(reset, new_user):  # pylint: disable=W0613
    '''Test that user_all returns the number of registered users'''

    user = new_user(email='user_1@email.com')
    users_all_input = {'token': user['token']}

    users_all = requests.get(f'{BASE_URL}/users/all',
                             params=users_all_input).json()
    assert len(users_all['users']) == 1

    new_user(email='user_2@email.com')
    users_all = requests.get(f'{BASE_URL}/users/all',
                             params=users_all_input).json()
    assert len(users_all['users']) == 2

    new_user(email='user_3@email.com')
    users_all = requests.get(f'{BASE_URL}/users/all',
                             params=users_all_input).json()
    assert len(users_all['users']) == 3


def test_users_all_invalid_token(reset, invalid_token):  # pylint: disable=W0613
    '''Test user_all with invalid token'''

    users_all_input = {'token': invalid_token}
    error = requests.get(f'{BASE_URL}/users/all', params=users_all_input)

    with pytest.raises(requests.HTTPError):
        requests.Response.raise_for_status(error)
