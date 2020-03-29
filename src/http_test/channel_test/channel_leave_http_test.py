'''
HTTP Tests for the channel_leave function.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_leave_new(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing channel leave function for a public channel.
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

    requests.post(f'{BASE_URL}/channel/leave', json=input_dict)

    details_in = {
        'token': user1['token'],
        'channel_id': channel['channel_id']
    }

    details = requests.get(
        f'{BASE_URL}/channel/details', params=details_in).json()

    assert len(details['all_members']) == 1


def test_leave_ch(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing channel leave function for an invalid channel_id
    '''

    user = new_user()

    new_channel(user)

    input_dict = {
        'token': user['token'],
        'channel_id': -1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/leave',
                      json=input_dict).raise_for_status()


def test_leave_owner(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing channel leave for owner member.
    '''

    user = new_user()
    user2 = new_user()

    channel = new_channel(user)

    join_dict = {
        'token': user2['token'],
        'channel_id': channel['channel_id']
    }

    # user2 joins the channel.
    requests.post(f'{BASE_URL}/channel/join', json=join_dict)

    leave_dict = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }

    # user leaves the channel.
    requests.post(f'{BASE_URL}/channel/leave', json=leave_dict)

    # user2 gets details of channel.
    details = requests.get(
        f'{BASE_URL}/channel/details', params=join_dict).json()

    assert len(details['owner_members']) == 0


def test_leave_member(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing channel leave for non-member.
    '''

    user = new_user()
    user2 = new_user()

    channel = new_channel(user)

    input_dict = {
        'token': user2['token'],
        'channel_id': channel['channel_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/leave',
                      json=input_dict).raise_for_status()
