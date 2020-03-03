import pytest
import auth
import channel
import channels
from error import InputError, AccessError


@pytest.fixture
def user():
    return auth.auth_register('user.name@email.com', 'password', 'First',
                              'Last')


def test_create_public(user):
    '''Test that any users can join a public channel'''
    test_channel = channels.channels_create(user['token'], 'Channel', True)
    channel.channel_join(user['token'], test_channel['channel_id'])
    details = channel.channel_details(user['token'],
                                      test_channel['channel_id'])
    assert user['u_id'] == details['all_members'][0]['u_id']


def test_create_private(user):
    '''Test that an unauthorised user cannot join a private channel'''
    test_channel = channels.channels_create(user['token'], 'Channel', False)
    with pytest.raises(AccessError) as e:
        channel.channel_join(user['token'], test_channel['channel_id'])
    details = channel.channel_details(user['token'],
                                      test_channel['channel_id'])
    assert len(details['all_members']) == 0


def test_create_types(user):
    '''Test the types returned by channels_user'''
    channel = channels.channels_create(user['token'], 'Channel', True)
    assert isinstance(channel, dict) == True
    assert isinstance(channel['channel_id'], int) == True


def test_create_long_name(user):
    '''Test creation of channel with name length > 20'''
    with pytest.raises(InputError) as e:
        channels.channels_create(user['token'], 'i' * 21, True)


def test_listall(user):
    '''Test that all created channels are returned by channels_listall'''
    channel_1 = channels.channels_create(user['token'], 'One', True)
    channel_2 = channels.channels_create(user['token'], 'Two', True)
    channel_3 = channels.channels_create(user['token'], 'Three', True)

    all_channels = channels.channels_listall(user['token'])['channels']
    assert isinstance(all_channels, list) == True

    channel_ids = [
        channel_1['channel_id'], channel_2['channel_id'],
        channel_3['channel_id']
    ]

    for channel in all_channels:
        assert channel['channel_id'] in channel_ids


def test_list(user):
    '''Test that channels_list only returns channels the user is in'''
    joined_1 = channels.channels_create(user['token'], 'One', True)
    joined_2 = channels.channels_create(user['token'], 'Two', True)
    not_joined = channels.channels_create(user['token'], 'Three', True)

    channel.channel_join(user['token'], joined_1['channel_id'])
    channel.channel_join(user['token'], joined_2['channel_id'])

    joined_channel_ids = [joined_1['channel_id'], joined_2['channel_id']]

    all_joined_channels = channels.channels_list(user['token'])['channels']
    assert isinstance(all_joined_channels, list) == True
    assert len(all_joined_channels) == 2

    for chan in all_joined_channels:
        assert chan['channel_id'] in joined_channel_ids
        assert chan['channel_id'] != not_joined['channel_id']
