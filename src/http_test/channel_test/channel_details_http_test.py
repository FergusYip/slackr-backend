'''
HTTP Tests for the channel_details function.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_details_owner(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Checking if channel has dummy_user1 in owner_members.
    '''

    user = new_user()
    channel = new_channel(user)

    input_dict = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }

    details = requests.get(
        f'{BASE_URL}/channel/details', params=input_dict).json()

    assert len(details['owner_members']) == 1


def test_details_added_owner(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Adding owners to a channel and checking if the channel has 2 owners.
    '''

    user1 = new_user()
    user2 = new_user(email='something@google.com')
    channel = new_channel(user1)

    addowner_in = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user2['u_id']
    }

    details_in = {
        'token': user1['token'],
        'channel_id': channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/addowner', json=addowner_in)

    details = requests.get(
        f'{BASE_URL}/channel/details', params=details_in).json()

    assert len(details['owner_members']) == 2


def test_details_all(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Checking if channels have 1 user in all_members.
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


def test_invalid_ch(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing case when channel ID is invalid.
    '''

    user = new_user()
    new_channel(user)

    input_dict = {
        'token': user['token'],
        'channel_id': -1
    }

    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/channel/details',
                     params=input_dict).raise_for_status()


def test_invalid_user(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing case when user not in channel.
    '''

    user1 = new_user()
    user2 = new_user()
    channel = new_channel(user1)

    input_dict = {
        'token': user2['token'],
        'channel_id': channel['channel_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/channel/details',
                     params=input_dict).raise_for_status()
