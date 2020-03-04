import pytest
import auth
import channel
import channels


@pytest.fixture
def test_user():
    return auth.auth_register('test.user@email.com', 'password', 'First',
                              'Last')


@pytest.fixture
def invalid_token(test_user):
    assert auth.auth_logout(test_user['token'])
    return test_user['token']


@pytest.fixture
def test_channel(test_user):
    return channels.channels_create(test_user['token'], 'Channel', True)


@pytest.fixture
def new_user():
    def _new_user(email):
        return auth.auth_register(email, 'password', 'First', 'Last')

    return _new_user


@pytest.fixture
def make_join_channel():
    def _make_join_channel(target_user, channel_name):
        ch = channels.channels_create(target_user['token'], target_user, True)
        channel.channel_join(target_user['token'], ch['channel_id'])
        return ch

    return _make_join_channel
