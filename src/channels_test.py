import pytest
import auth
import channel
import channels
from error import InputError, AccessError


def test_create_public(test_user):
    '''Test that any users can join a public channel'''

    test_channel = channels.channels_create(test_user['token'], 'Channel',
                                            True)
    channel.channel_join(test_user['token'], test_channel['channel_id'])
    details = channel.channel_details(test_user['token'],
                                      test_channel['channel_id'])
    assert test_user['u_id'] == details['all_members'][0]['u_id']


def test_create_private(test_user):
    '''Test that an unauthorised user cannot join a private channel'''

    test_channel = channels.channels_create(test_user['token'], 'Channel',
                                            False)
    with pytest.raises(AccessError):
        channel.channel_join(test_user['token'], test_channel['channel_id'])
    details = channel.channel_details(test_user['token'],
                                      test_channel['channel_id'])
    assert len(details['all_members']) == 0


def test_create_types(test_user):
    '''Test the types returned by channels_user'''

    channel = channels.channels_create(test_user['token'], 'Channel', True)
    assert isinstance(channel, dict) == True
    assert isinstance(channel['channel_id'], int) == True


def test_create_long_name(test_user):
    '''Test creation of channel with name length > 20'''

    with pytest.raises(InputError):
        channels.channels_create(test_user['token'], 'i' * 21, True)


def test_create_invalid_token(invalid_token):
    '''Test that channels_create raises an AccessError when given invalid token'''
    with pytest.raises(AccessError):
        channels.channels_create(invalid_token, 'Channel', True)


def test_listall(test_user):
    '''Test that all created channels are returned by channels_listall'''

    channel_1 = channels.channels_create(test_user['token'], 'One', True)
    channel_2 = channels.channels_create(test_user['token'], 'Two', True)
    channel_3 = channels.channels_create(test_user['token'], 'Three', True)

    all_channels = channels.channels_listall(test_user['token'])['channels']
    assert isinstance(all_channels, list) == True

    channel_ids = [
        channel_1['channel_id'], channel_2['channel_id'],
        channel_3['channel_id']
    ]

    for channel in all_channels:
        assert channel['channel_id'] in channel_ids


def test_listall_no_channels(test_user):
    '''Test that channels_listall doesn't return any channels when there aren't any'''

    all_channels = channels.channels_listall(test_user['token'])['channels']
    assert len(all_channels) == 0


def test_listall_invalid_token(invalid_token):
    '''Test that channels_create raises an AccessError when given invalid token'''
    with pytest.raises(AccessError):
        channels.channels_listall(invalid_token)


def test_list(test_user):
    '''Test that channels_list only returns channels the user is in'''

    joined_1 = channels.channels_create(test_user['token'], 'One', True)
    joined_2 = channels.channels_create(test_user['token'], 'Two', True)
    not_joined = channels.channels_create(test_user['token'], 'Three', True)

    channel.channel_join(test_user['token'], joined_1['channel_id'])
    channel.channel_join(test_user['token'], joined_2['channel_id'])

    joined_channel_ids = [joined_1['channel_id'], joined_2['channel_id']]

    all_joined_channels = channels.channels_list(
        test_user['token'])['channels']
    assert isinstance(all_joined_channels, list) == True
    assert len(all_joined_channels) == 2

    for chan in all_joined_channels:
        assert chan['channel_id'] in joined_channel_ids
        assert chan['channel_id'] != not_joined['channel_id']


def test_list_no_channels(test_user):
    '''Test that channels_list doesn't return any channels when there aren't any'''

    all_channels = channels.channels_list(test_user['token'])['channels']
    assert len(all_channels) == 0


def test_list_invalid_token(invalid_token):
    '''Test that channels_list raises an AccessError when given invalid token'''
    with pytest.raises(AccessError):
        channels.channels_list(invalid_token)