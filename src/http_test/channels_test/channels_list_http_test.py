'''Pytest script for testing /channels/list route'''
import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_list_return_type(reset, new_user, new_channel):  # pylint: disable=W0613
    '''Test that the types of return values are as expected'''
    user = new_user()
    new_channel(user, 'Channel')

    list_input = {'token': user['token']}
    channels_list = requests.get(f'{BASE_URL}/channels/list',
                                 params=list_input).json()['channels']

    assert isinstance(channels_list, list)
    assert isinstance(channels_list[0], dict)
    assert isinstance(channels_list[0]['channel_id'], int)
    assert isinstance(channels_list[0]['name'], str)


def test_list(reset, new_user, new_channel):  # pylint: disable=W0613
    '''Test that channels_list only returns channels the user is in'''

    user_1 = new_user(email='user_1@email.com')
    user_2 = new_user(email='user_2@email.com')

    new_channel(user_1, 'User 1 Channel')

    list_input_1 = {'token': user_1['token']}
    user_1_channels = requests.get(f'{BASE_URL}/channels/list',
                                   params=list_input_1).json()

    list_input_2 = {'token': user_2['token']}
    user_2_channels = requests.get(f'{BASE_URL}/channels/list',
                                   params=list_input_2).json()

    assert len(user_1_channels['channels']) == 1
    assert len(user_2_channels['channels']) == 0


def test_list_no_channels(reset, new_user):  # pylint: disable=W0613
    '''Test that channels_list doesn't return any channels when there aren't any'''
    user = new_user()
    list_input = {'token': user['token']}
    channels_list = requests.get(f'{BASE_URL}/channels/list',
                                 params=list_input).json()['channels']
    assert len(channels_list) == 0


def test_list_invalid_token(reset, invalid_token):  # pylint: disable=W0613
    '''Test that channels_list raises an HTTPError when given invalid token'''
    list_input = {'token': invalid_token}
    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/channels/list',
                     params=list_input).raise_for_status()
