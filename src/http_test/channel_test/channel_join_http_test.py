'''
HTTP Tests for the channel_invite function.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_join_new(reset, new_user, new_channel):
    '''
    Testing channel join function for a public channel.
    '''

    user1 = new_user()
    user2 = new_user()

    channel = new_channel(user1)

    input_dict = {
        'token': user2['token'],
        'channel_id': channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/join', json=input_dict)

    details = requests.get(
        f'{BASE_URL}/channel/details', params=input_dict).json()

    assert len(details['all_members']) == 2


def test_join_id(reset, new_user, new_channel):
    '''
    Testing channel join function for an invalid channel_id
    '''

    user1 = new_user()
    user2 = new_user()

    channel = new_channel(user1)

    input_dict = {
        'token': user2['token'],
        'channel_id': -1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/join',
                      json=input_dict).raise_for_status()


def test_join_private(reset, new_user, new_channel):

    user1 = new_user()
    channel = new_channel(user1, is_public=False)
