import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_workspace_reset_user(reset, new_user):
    user_a = new_user(email='user_a@email.com')
    user_b = new_user(email='user_b@email.com')
    all_users = requests.get(f'{BASE_URL}/users/all')
    assert len(all_users['users']) == 2

    requests.post(f'{BASE_URL}/workspace/reset')

    user_c = new_user(email='user_c@email.com')

    all_users = requests.get(f'{BASE_URL}/users/all').json()

    assert len(all_users['users']) == 1


def test_workspace_reset_channels(reset, new_user, new_channel):
    user = new_user()
    new_channel(user, 'Channel A')
    new_channel(user, 'Channel B')

    channels_listall_input = {'token': user['token']}

    all_channels = requests.get(f'{BASE_URL}/channels/listall',
                                json=channels_listall_input).json()

    assert len(all_channels['channels']) == 2

    requests.post(f'{BASE_URL}/workspace/reset')

    user = new_user()
    channels_listall_input = {'token': user['token']}
    all_channels = requests.get(f'{BASE_URL}/channels/listall',
                                json=channels_listall_input).json()

    assert len(all_channels['channels']) == 0


def test_workspace_reset_token_blacklist(reset, new_user):
    user = new_user()

    requests.post(f'{BASE_URL}/workspace/reset')

    logout_input = {'token': user['token']}

    # Following line raises error as u_id in token payload does not belong to a user
    error = requests.post(f'{BASE_URL}/auth/logout', json=logout_input)

    with pytest.raises(requests.HTTPError):
        requests.Response.raise_for_status(error)
