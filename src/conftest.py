import pytest
import auth
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