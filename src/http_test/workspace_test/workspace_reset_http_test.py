'''Pytest script for testing /workspace/reset route'''
import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_workspace_reset_user(reset, new_user):
    '''Test that the number of users are reset'''
    user_a = new_user(email='user_a@email.com')
    new_user(email='user_b@email.com')

    users_all_input = {'token': user_a['token']}
    all_users = requests.get(f'{BASE_URL}/users/all',
                             params=users_all_input).json()

    assert len(all_users['users']) == 2

    requests.post(f'{BASE_URL}/workspace/reset')

    user_c = new_user(email='user_c@email.com')

    users_all_input = {'token': user_c['token']}
    all_users = requests.get(f'{BASE_URL}/users/all',
                             params=users_all_input).json()

    assert len(all_users['users']) == 1


def test_workspace_reset_channels(reset, new_user, new_channel):
    '''Test that the number of channels is reset'''
    user = new_user()
    new_channel(user, 'Channel A')
    new_channel(user, 'Channel B')

    channels_listall_input = {'token': user['token']}

    all_channels = requests.get(f'{BASE_URL}/channels/listall',
                                params=channels_listall_input).json()

    assert len(all_channels['channels']) == 2

    requests.post(f'{BASE_URL}/workspace/reset')

    user = new_user()
    channels_listall_input = {'token': user['token']}
    all_channels = requests.get(f'{BASE_URL}/channels/listall',
                                params=channels_listall_input).json()

    assert len(all_channels['channels']) == 0


def test_workspace_reset_old_token(reset, new_user):
    '''Test that the old tokens are invalid is reset'''
    user = new_user()

    requests.post(f'{BASE_URL}/workspace/reset')

    logout_input = {'token': user['token']}

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/auth/logout',
                      json=logout_input).raise_for_status()
