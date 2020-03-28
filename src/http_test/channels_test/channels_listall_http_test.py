'''Pytest script for testing /channels/listall route'''
import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_listall_return_type(reset, new_user, new_channel):  # pylint: disable=W0613
    '''Test that the types of return values are as expected'''
    user = new_user()
    new_channel(user, 'Channel')

    listall_input = {'token': user['token']}
    channels_list = requests.get(f'{BASE_URL}/channels/listall',
                                 params=listall_input).json()['channels']

    assert isinstance(channels_list, list)
    assert isinstance(channels_list[0], dict)
    assert isinstance(channels_list[0]['channel_id'], int)
    assert isinstance(channels_list[0]['name'], str)


def test_listall(reset, new_user, new_channel):  # pylint: disable=W0613
    '''Test that all created channels are returned by channels_listall'''
    user = new_user()
    channel_1 = new_channel(user, 'Channel One')
    channel_2 = new_channel(user, 'Channel Two')
    channel_3 = new_channel(user, 'Channel Three')

    listall_input = {'token': user['token']}
    all_channels = requests.get(f'{BASE_URL}/channels/listall',
                                params=listall_input).json()['channels']

    channel_ids = [
        channel_1['channel_id'], channel_2['channel_id'],
        channel_3['channel_id']
    ]

    for channel in all_channels:
        assert channel['channel_id'] in channel_ids


def test_listall_no_channels(reset, new_user):  # pylint: disable=W0613
    '''Test that channels_listall doesn't return any channels when there aren't any'''

    user = new_user()
    listall_input = {'token': user['token']}
    channels_list = requests.get(f'{BASE_URL}/channels/listall',
                                 params=listall_input).json()['channels']
    assert len(channels_list) == 0


def test_listall_invalid_token(reset, invalid_token):  # pylint: disable=W0613
    '''Test that channels_listall raises an HTTPError when given invalid token'''
    listall_input = {'token': invalid_token}
    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/channels/listall',
                     params=listall_input).raise_for_status()


def test_listall_insufficient_params(reset):  # pylint: disable=W0613
    '''Test input of invalid parameters into channels_listall'''

    with pytest.raises(requests.HTTPError):
        requests.post(f"{BASE_URL}/channels/listall",
                      params={}).raise_for_status()
