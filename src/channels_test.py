import auth
import channels
import pytest
from error import InputError, AccessError


def test_create():
    user = auth.register('user.name@email.com', 'password', 'First', 'Last')
    channel = channels.create(user['token'], 'Channel', True)
    assert isinstance(channel, dict) == True
    assert isinstance(channel['channel_id'], int) == True


def test_create_long_name():
    user = auth.register('user.name@email.com', 'password', 'First', 'Last')
    with pytest.raises(InputError) as e:
        channel = channels.create(user['token'], 'i' * 21, True)
