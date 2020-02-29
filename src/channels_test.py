import auth
import channel
import channels
import pytest
from error import InputError


@pytest.fixture
def user():
    return auth.register('user.name@email.com', 'password', 'First', 'Last')


def test_create(user):
    channel = channels.create(user['token'], 'Channel', True)
    assert isinstance(channel, dict) == True
    assert isinstance(channel['channel_id'], int) == True


def test_create_long_name(user):
    with pytest.raises(InputError) as e:
        channel = channels.create(user['token'], 'i' * 21, True)


def test_listall(user):
    channel_1 = channels.create(user['token'], 'One', True)
    channel_2 = channels.create(user['token'], 'Two', True)
    channel_3 = channels.create(user['token'], 'Three', True)

    all_channels = channels.listall(user['token'])['channels']
    assert isinstance(all_channels, list) == True

    channel_ids = [
        channel_1['channel_id'], channel_2['channel_id'],
        channel_3['channel_id']
    ]

    for channel in all_channels:
        assert channel['channel_id'] in channel_ids


def test_list(user):
    joined_1 = channels.create(user['token'], 'One', True)
    joined_2 = channels.create(user['token'], 'Two', True)
    not_joined = channels.create(user['token'], 'Three', True)

    channel.channel_join(user['token'], joined_1['channel_id'])
    channel.channel_join(user['token'], joined_2['channel_id'])

    joined_channel_ids = [joined_1['channel_id'], joined_2['channel_id']]

    all_joined_channels = channels.list(user['token'])['channels']
    assert isinstance(all_joined_channels, list) == True
    assert len(all_joined_channels) == 2

    for chan in all_joined_channels:
        assert chan['channel_id'] in joined_channel_ids
        assert chan['channel_id'] != not_joined['channel_id']
