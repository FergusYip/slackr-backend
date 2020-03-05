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
    assert isinstance(channel, dict)
    assert isinstance(channel['channel_id'], int)


def test_create_long_name(test_user):
    '''Test creation of channel with name length > 20'''

    with pytest.raises(InputError):
        channels.channels_create(test_user['token'], 'i' * 21, True)


def test_create_invalid_token(invalid_token):
    '''Test that channels_create raises an AccessError when given invalid token'''
    with pytest.raises(AccessError):
        channels.channels_create(invalid_token, 'Channel', True)
