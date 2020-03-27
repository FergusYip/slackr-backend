import json
import urllib
import requests
import pytest

BASE_URL = 'http://127.0.0.1'
PORT = '8080'


@pytest.fixture
def reset():
    '''Fixture for resetting the workspace'''
    requests.post(f"{BASE_URL}:{PORT}/workspace/reset")


@pytest.fixture
def new_user():
    '''Factory as a fixture for a creating a new user with a specified email'''
    def _new_user(email='valid@email.com',
                  password='password',
                  name_first='First',
                  name_last='Last'):
        user_info = {
            'email': email,
            'password': password,
            'name_first': name_first,
            'name_last': name_last
        }
        user = requests.post(f"{BASE_URL}:{PORT}/auth/register",
                             json=user_info).json()
        return user

    return _new_user


@pytest.fixture
def invalid_token(new_user):
    '''Fixture for a creating an invalid token'''
    user = new_user()
    token = user['token']
    requests.post(f"{BASE_URL}:{PORT}/auth/logout", json={'token': token})
    return token


@pytest.fixture
def new_channel():
    '''Factory as a fixture for a test user to create a new channel and joining it'''
    def _new_channel(target_user, channel_name='Channel Name'):
        channel_info = {
            'token': target_user['token'],
            'channel_name': channel_name,
            'is_public': True
        }
        channel = requests.post(f"{BASE_URL}:{PORT}/channels/create",
                                json=channel_info).json()
        return channel

    return _new_channel


@pytest.fixture
def get_user_profile():
    '''Factory as a fixture for a retrieving user info'''
    def _get_user_profile(token, u_id):
        query_string = urllib.parse.urlencode({'token': token, 'u_id': u_id})
        user_profile = requests.get(
            f"{BASE_URL}:{PORT}/user/profile?{query_string}").json()
        return user_profile

    return _get_user_profile


@pytest.fixture
def send_msg():
    '''Factory as a fixture for a test user to create a new channel and joining it'''
    def _send_msg(token, channel_id, message):
        message_input = {
            'token': token,
            'channel_id': channel_id,
            'message': message
        }
        message = requests.post(f'{BASE_URL}/message/send',
                                json=message_input).json()
        return message

    return _send_msg


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
