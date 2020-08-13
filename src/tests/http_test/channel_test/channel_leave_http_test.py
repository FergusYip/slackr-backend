'''
HTTP Tests for the channel_leave function.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_leave_new(reset, new_user, new_channel):
    '''
    Testing channel leave function for a public channel.
    '''

    user1 = new_user(email='user_1@email.com')
    user2 = new_user(email='user_2@email.com')

    channel = new_channel(user1)

    input_dict = {'token': user2['token'], 'channel_id': channel['channel_id']}

    requests.post(f'{BASE_URL}/channel/join', json=input_dict)

    details = requests.get(f'{BASE_URL}/channel/details',
                           params=input_dict).json()

    assert len(details['all_members']) == 2

    requests.post(f'{BASE_URL}/channel/leave', json=input_dict)

    details_in = {'token': user1['token'], 'channel_id': channel['channel_id']}

    details = requests.get(f'{BASE_URL}/channel/details',
                           params=details_in).json()

    assert len(details['all_members']) == 1


def test_leave_ch(reset, new_user, new_channel):
    '''
    Testing channel leave function for an invalid channel_id
    '''

    user = new_user()

    new_channel(user)

    input_dict = {'token': user['token'], 'channel_id': -1}

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/leave',
                      json=input_dict).raise_for_status()


def test_leave_owner(reset, new_user, new_channel):
    '''
    Testing channel leave for owner member.
    '''

    user1 = new_user(email='user_1@email.com')
    user2 = new_user(email='user_2@email.com')

    channel = new_channel(user1)

    join_dict = {'token': user2['token'], 'channel_id': channel['channel_id']}

    # user2 joins the channel.
    requests.post(f'{BASE_URL}/channel/join', json=join_dict)

    leave_dict = {'token': user1['token'], 'channel_id': channel['channel_id']}

    # user leaves the channel.
    requests.post(f'{BASE_URL}/channel/leave', json=leave_dict)

    # user2 gets details of channel.
    details = requests.get(f'{BASE_URL}/channel/details',
                           params=join_dict).json()

    assert not details['owner_members']


def test_leave_member(reset, new_user, new_channel):
    '''
    Testing channel leave for non-member.
    '''

    user1 = new_user(email='user_1@email.com')
    user2 = new_user(email='user_2@email.com')

    channel = new_channel(user1)

    input_dict = {'token': user2['token'], 'channel_id': channel['channel_id']}

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/leave',
                      json=input_dict).raise_for_status()


def test_leave_insufficient_params(reset):
    '''Test input of invalid parameters into leave'''

    with pytest.raises(requests.HTTPError):
        requests.post(f"{BASE_URL}/channel/leave", json={}).raise_for_status()
