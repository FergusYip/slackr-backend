'''
HTTP Tests for the channel_details function.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_details_owner(reset, new_user, new_channel):
    '''
    Checking if channel has dummy_user1 in owner_members.
    '''

    user = new_user()
    channel = new_channel(user)

    input_dict = {'token': user['token'], 'channel_id': channel['channel_id']}

    details = requests.get(f'{BASE_URL}/channel/details',
                           params=input_dict).json()

    assert len(details['owner_members']) == 1


def test_details_added_owner(reset, new_user, new_channel,
                             get_channel_details):
    '''
    Adding owners to a channel and checking if the channel has 2 owners.
    '''

    user1 = new_user()
    user2 = new_user(email='something@google.com')
    channel = new_channel(user1)

    join_input = {'token': user2['token'], 'channel_id': channel['channel_id']}

    requests.post(f'{BASE_URL}/channel/join', json=join_input)

    addowner_in = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user2['u_id']
    }

    requests.post(f'{BASE_URL}/channel/addowner', json=addowner_in)

    details = get_channel_details(user1['token'], channel['channel_id'])

    assert len(details['owner_members']) == 2


def test_details_all(reset, new_user, new_channel):
    '''
    Checking if channels have 1 user in all_members.
    '''

    user1 = new_user(email='user_1@email.com')
    user2 = new_user(email='user_2@email.com')
    channel = new_channel(user1)

    input_dict = {'token': user2['token'], 'channel_id': channel['channel_id']}

    requests.post(f'{BASE_URL}/channel/join', json=input_dict)

    details = requests.get(f'{BASE_URL}/channel/details',
                           params=input_dict).json()

    assert len(details['all_members']) == 2


def test_invalid_ch(reset, new_user, new_channel):
    '''
    Testing case when channel ID is invalid.
    '''

    user = new_user()
    new_channel(user)

    input_dict = {'token': user['token'], 'channel_id': -1}

    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/channel/details',
                     params=input_dict).raise_for_status()


def test_invalid_user(reset, new_user, new_channel):
    '''
    Testing case when user not in channel.
    '''

    user1 = new_user(email='user_1@email.com')
    user2 = new_user(email='user_2@email.com')
    channel = new_channel(user1)

    input_dict = {'token': user2['token'], 'channel_id': channel['channel_id']}

    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/channel/details',
                     params=input_dict).raise_for_status()


def test_details_insufficient_params(reset):
    '''Test input of invalid parameters into details'''

    with pytest.raises(requests.HTTPError):
        requests.get(f"{BASE_URL}/channel/details",
                     params={}).raise_for_status()
