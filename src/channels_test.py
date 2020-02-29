import auth
import channels
import pytest
from error import InputError


def test_create():
    user = auth.register('user.name@email.com', 'password', 'First', 'Last')
    channel = channels.create(user['token'], 'Channel', True)
    assert isinstance(channel, dict) == True
    assert isinstance(channel['channel_id'], int) == True


def test_create_long_name():
    user = auth.register('user.name@email.com', 'password', 'First', 'Last')
    with pytest.raises(InputError) as e:
        channel = channels.create(user['token'], 'i' * 21, True)


def test_listall():
    user = auth.register('user.name@email.com', 'password', 'First', 'Last')
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