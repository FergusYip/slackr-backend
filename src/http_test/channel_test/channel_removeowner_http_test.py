'''
HTTP Tests for the channel_removeowner function.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_removeowner(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing the removeowner function on a public channel.
    '''

    user1 = new_user(email='user_1@email.com')
    user2 = new_user(email='user_2@email.com')
    channel = new_channel(user1)

    input_dict = {'token': user2['token'], 'channel_id': channel['channel_id']}

    # user2 joins channel.
    requests.post(f'{BASE_URL}/channel/join', json=input_dict)

    details = requests.get(f'{BASE_URL}/channel/details',
                           params=input_dict).json()

    assert len(details['owner_members']) == 1

    add_dict = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user2['u_id']
    }

    # adding user2 as owner of channel.
    requests.post(f'{BASE_URL}/channel/addowner', json=add_dict)

    details = requests.get(f'{BASE_URL}/channel/details',
                           params=input_dict).json()

    assert len(details['owner_members']) == 2

    # removing user2 as owner of channel.
    requests.post(f'{BASE_URL}/channel/removeowner', json=add_dict)

    details = requests.get(f'{BASE_URL}/channel/details',
                           params=input_dict).json()

    assert len(details['owner_members']) == 1


def test_empty_owner(reset, new_user, new_channel, get_channel_details):  # pylint: disable=W0613
    '''
    Testing removeowner when the only owner removes himself as owner.
    '''

    user1 = new_user(email='user_1@email.com')
    channel = new_channel(user1)

    input_dict = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user1['u_id']
    }

    requests.post(f'{BASE_URL}/channel/removeowner', json=input_dict)

    details = get_channel_details(user1['token'], channel['channel_id'])

    assert len(details['owner_members']) == 0
    assert len(details['all_members']) == 1


def test_not_owner(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing the removeowner function when authorized user is not an owner of
    channel
    '''

    user1 = new_user(email='user_1@email.com')
    user2 = new_user(email='user_2@email.com')
    channel = new_channel(user1)

    input_dict = {
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'u_id': user1['u_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/removeowner',
                      json=input_dict).raise_for_status()


def test_invalid_ch(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing the removeowner function when an invalid channel id is passed.
    '''

    user1 = new_user(email='user_1@email.com')
    user2 = new_user(email='user_2@email.com')
    new_channel(user1)

    input_dict = {
        'token': user1['token'],
        'channel_id': -1,
        'u_id': user2['u_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/removeowner',
                      json=input_dict).raise_for_status()


def test_invalid_uid(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing the removeowner function when an invalid user id is passed.
    '''

    user = new_user()
    channel = new_channel(user)

    input_dict = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'u_id': -1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/removeowner',
                      json=input_dict).raise_for_status()
