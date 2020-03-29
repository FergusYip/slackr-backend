'''
HTTP Tests for the channel_invite function.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_invite_channel(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing channel invite for a public channel.
    '''

    user1 = new_user()
    user2 = new_user(email='something@google.com')

    channel = new_channel(user1)

    input_dict = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user2['u_id']
    }

    requests.post(f'{BASE_URL}/channel/invite', json=input_dict)

    details_in = {'token': user1['token'], 'channel_id': channel['channel_id']}

    details = requests.get(f'{BASE_URL}/channel/details',
                           params=details_in).json()

    assert len(details['all_members']) == 2


def test_invalid_user(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing channel invite function for a non-existent user.
    '''

    user1 = new_user()

    channel = new_channel(user1)

    input_dict = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'u_id': 2
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/invite',
                      json=input_dict).raise_for_status()


def test_invalid_channel(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing channel invite for a non-existent channel.
    '''
    user1 = new_user()
    user2 = new_user(email='something@google.com')

    new_channel(user1)

    input_dict = {
        'token': user1['token'],
        'channel_id': -1,
        'u_id': user2['u_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/invite',
                      json=input_dict).raise_for_status()


def test_invite_access(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing case when inviting user is not a member of a channel
    '''

    user1 = new_user()
    user2 = new_user(email='something@google.com')

    channel = new_channel(user1)

    input_dict = {
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'u_id': user1['u_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/invite',
                      json=input_dict).raise_for_status()
