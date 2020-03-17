import pytest
import auth
import channel
import channels
from error import InputError, AccessError


def test_listall(test_user):
    '''Test that all created channels are returned by channels_listall'''

    channel_1 = channels.channels_create(test_user['token'], 'One', True)
    channel_2 = channels.channels_create(test_user['token'], 'Two', True)
    channel_3 = channels.channels_create(test_user['token'], 'Three', True)

    all_channels = channels.channels_listall(test_user['token'])['channels']

    channel_ids = [
        channel_1['channel_id'], channel_2['channel_id'],
        channel_3['channel_id']
    ]

    for channel in all_channels:
        assert channel['channel_id'] in channel_ids


def test_listall_return_type(test_user, make_join_channel):
    test_channel = make_join_channel(test_user, 'Channel')
    all_channels = channels.channels_listall(test_user['token'])['channels']
    assert isinstance(all_channels, list)
    assert isinstance(all_channels[0], dict)
    assert isinstance(all_channels[0]['channel_id'], int)
    assert isinstance(all_channels[0]['name'], str)


def test_listall_no_channels(test_user):
    '''Test that channels_listall doesn't return any channels when there aren't any'''

    all_channels = channels.channels_listall(test_user['token'])['channels']
    assert len(all_channels) == 0


def test_listall_invalid_token(invalid_token):
    '''Test that channels_create raises an AccessError when given invalid token'''
    with pytest.raises(AccessError):
        channels.channels_listall(invalid_token)
