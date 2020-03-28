''' System tests for channels_list'''
import pytest
import channel
import channels
from error import AccessError


def test_list(reset, test_user):  # pylint: disable=W0613
    '''Test that channels_list only returns channels the user is in'''

    joined_1 = channels.channels_create(test_user['token'], 'One', True)
    joined_2 = channels.channels_create(test_user['token'], 'Two', True)
    not_joined = channels.channels_create(test_user['token'], 'Three', True)

    channel.channel_join(test_user['token'], joined_1['channel_id'])
    channel.channel_join(test_user['token'], joined_2['channel_id'])

    joined_channel_ids = [joined_1['channel_id'], joined_2['channel_id']]

    joined_channels = channels.channels_list(test_user['token'])['channels']
    assert len(joined_channels) == 2

    for chan in joined_channels:
        assert chan['channel_id'] in joined_channel_ids
        assert chan['channel_id'] != not_joined['channel_id']


def test_list_return_type(reset, test_user, new_channel):  # pylint: disable=W0613
    '''Test that the types of the values returned are correct'''
    new_channel(test_user, 'Channel')
    all_channels = channels.channels_list(test_user['token'])['channels']
    assert isinstance(all_channels, list)
    assert isinstance(all_channels[0], dict)
    assert isinstance(all_channels[0]['channel_id'], int)
    assert isinstance(all_channels[0]['name'], str)


def test_list_no_channels(reset, test_user):  # pylint: disable=W0613
    '''Test that channels_list doesn't return any channels when there aren't any'''

    all_channels = channels.channels_list(test_user['token'])['channels']
    assert len(all_channels) == 0


def test_list_invalid_token(reset, invalid_token):  # pylint: disable=W0613
    '''Test that channels_list raises an AccessError when given invalid token'''
    with pytest.raises(AccessError):
        channels.channels_list(invalid_token)
