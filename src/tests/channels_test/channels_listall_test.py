''' System tests for channels_listall'''
import pytest
import channels
from error import AccessError, InputError


def test_listall(reset, test_user):  # pylint: disable=W0613
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


def test_listall_return_type(reset, test_user, new_channel):  # pylint: disable=W0613
    '''Test that the types of the values returned are correct'''
    new_channel(test_user, 'Channel')
    all_channels = channels.channels_listall(test_user['token'])['channels']
    assert isinstance(all_channels, list)
    assert isinstance(all_channels[0], dict)
    assert isinstance(all_channels[0]['channel_id'], int)
    assert isinstance(all_channels[0]['name'], str)


def test_listall_no_channels(reset, test_user):  # pylint: disable=W0613
    '''Test that channels_listall doesn't return any channels when there aren't any'''

    all_channels = channels.channels_listall(test_user['token'])['channels']
    assert len(all_channels) == 0


def test_listall_invalid_token(reset, invalid_token):  # pylint: disable=W0613
    '''Test that channels_create raises an AccessError when given invalid token'''
    with pytest.raises(AccessError):
        channels.channels_listall(invalid_token)


def test_listall_invalid_params(reset):  # pylint: disable=W0613
    '''Test input of invalid parameters into channels_listall'''

    with pytest.raises(InputError):
        channels.channels_listall(None)
