import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_list_return_type(reset, new_user, make_join_channel):
    user = new_user()
    make_join_channel(user, 'Channel')

    listall_input = {'token': user['token']}
    channels_list = requests.get(f'{BASE_URL}/channels/listall',
                                 json=listall_input).json()['channels']
    assert isinstance(channels_list, list)
    assert isinstance(channels_list[0], dict)
    assert isinstance(channels_list[0]['channel_id'], int)
    assert isinstance(channels_list[0]['name'], str)


def test_listall(reset, new_user, make_join_channel):
    '''Test that all created channels are returned by channels_listall'''
    user = new_user()
    channel_1 = make_join_channel(user, 'Channel One')
    channel_2 = make_join_channel(user, 'Channel Two')
    channel_3 = make_join_channel(user, 'Channel Three')

    listall_input = {'token': user['token']}
    all_channels = requests.get(f'{BASE_URL}/channels/listall',
                                json=listall_input).json()['channels']

    channel_ids = [
        channel_1['channel_id'], channel_2['channel_id'],
        channel_3['channel_id']
    ]

    for channel in all_channels:
        assert channel['channel_id'] in channel_ids


def test_listall_no_channels(reset, new_user):
    '''Test that channels_listall doesn't return any channels when there aren't any'''

    user = new_user()
    listall_input = {'token': user['token']}
    channels_list = requests.get(f'{BASE_URL}/channels/listall',
                                 json=listall_input).json()['channels']
    assert len(channels_list) == 0


def test_listall_invalid_token(reset, invalid_token):
    '''Test that channels_listall raises an HTTPError when given invalid token'''
    listall_input = {'token': invalid_token}
    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/channels/listall',
                     json=listall_input).raise_for_status()
