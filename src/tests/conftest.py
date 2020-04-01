'''Conftest file for system testing slackr'''
import pytest
import auth
import channels
import workspace


@pytest.fixture
def reset():
    '''Fixture for resetting the workspace'''
    workspace.workspace_reset()


@pytest.fixture
def test_user():
    '''Fixture for a creating a test user'''

    return auth.auth_register('test.user@email.com', 'password', 'First',
                              'Last')


@pytest.fixture
def invalid_token(test_user):
    '''Fixture for a creating an invalid token'''

    assert auth.auth_logout(test_user['token'])
    return test_user['token']


@pytest.fixture
def test_channel(test_user):
    '''Fixture for a creating a test channel'''

    return channels.channels_create(test_user['token'], 'Channel', True)


@pytest.fixture
def new_user():
    '''Factory as a fixture for a creating a new user with a specified email'''
    def _new_user(email='valid@email.com',
                  password='password',
                  name_first='First',
                  name_last='Last'):

        return auth.auth_register(email, password, name_first, name_last)

    return _new_user


@pytest.fixture
def new_channel():
    '''Factory as a fixture for a test user to create a new channel and joining it'''
    def _new_channel(target_user, name='Channel', is_public=True):
        return channels.channels_create(target_user['token'], name, is_public)

    return _new_channel


@pytest.fixture
def valid_emails():
    '''Fixture for a tuple of valid emails'''

    return ('latonyaDAVISON@email.com', '123456789@email.com',
            'lantonyDAVISON123@email.com', 'lantony_davison@email.com',
            'lantony.davison@email.com', 'lantony-davison@email.com')


@pytest.fixture
def invalid_emails():
    '''Fixture for a tuple of invalid emails'''

    return (
        '.latonyadavison@email.com',
        'latonyadavison.@email.com',
        'latonya..davison.@email.com',
        'latonya@davison@email.com',
        'latonyadavison.com',
    )
