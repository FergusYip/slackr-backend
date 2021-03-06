'''Pytest script for testing /channels/create route'''
import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_create_type(reset, new_user):
    '''Test the types of values returned by channels/create'''
    user = new_user()

    channel_info = {
        'token': user['token'],
        'name': 'Channel Name',
        'is_public': True
    }

    test_channel = requests.post(f'{BASE_URL}/channels/create',
                                 json=channel_info).json()

    assert isinstance(test_channel, dict)
    assert isinstance(test_channel['channel_id'], int)


def test_create_name(reset, new_user, get_channel_details):
    '''Test that the channel name matches input'''
    user = new_user()

    channel_name = 'Twenty Twenty'

    create_input = {
        'token': user['token'],
        'name': channel_name,
        'is_public': True
    }

    channel = requests.post(f'{BASE_URL}/channels/create',
                            json=create_input).json()

    details = get_channel_details(user['token'], channel['channel_id'])
    assert details['name'] == channel_name


def test_create_joined(reset, new_user, get_channel_details):
    '''Test the user who created the channel is a member and owner'''
    user = new_user()

    create_input = {
        'token': user['token'],
        'name': 'Channel Name',
        'is_public': True
    }

    channel = requests.post(f'{BASE_URL}/channels/create',
                            json=create_input).json()

    details = get_channel_details(user['token'], channel['channel_id'])

    owner_ids = [owner['u_id'] for owner in details['owner_members']]
    member_ids = [member['u_id'] for member in details['all_members']]

    assert user['u_id'] in owner_ids
    assert user['u_id'] in member_ids


def test_create_private(reset, new_user, get_channel_details):
    '''Test that an unauthorised user cannot join a private channel'''

    owner = new_user(email='owner@email.com')
    stranger = new_user(email='stranger@email.com')

    create_input = {
        'token': owner['token'],
        'name': 'Channel Name',
        'is_public': False
    }

    channel = requests.post(f'{BASE_URL}/channels/create',
                            json=create_input).json()

    join_input = {
        'token': stranger['token'],
        'channel_id': channel['channel_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channel/join',
                      json=join_input).raise_for_status()

    details = get_channel_details(owner['token'], channel['channel_id'])

    assert len(details['all_members']) == 1


def test_create_long_name(reset, new_user):
    '''Test creation of channel with name length > 20'''

    user = new_user()

    create_input = {
        'token': user['token'],
        'name': 'i' * 21,
        'is_public': True
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channels/create',
                      json=create_input).raise_for_status()


def test_create_invalid_token(reset, invalid_token):
    '''Test that channels_create raises an AccessError when given invalid token'''

    create_input = {
        'token': invalid_token,
        'name': 'Channel Name',
        'is_public': True
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channels/create',
                      json=create_input).raise_for_status()


def test_create_insufficient_params(reset):
    '''Test input of invalid parameters into channels_create'''

    with pytest.raises(requests.HTTPError):
        requests.post(f"{BASE_URL}/channels/create",
                      json={}).raise_for_status()
