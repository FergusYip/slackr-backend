import json
import requests
import urllib
import pytest
from error import AccessError, InputError

BASE_URL = 'http://127.0.0.1'
PORT = '8080'

# @pytest.fixture
# def reset():
#     '''Fixture for resetting the workspace'''
#     requests.get(f"{BASE_URL}/workspace/reset")


@pytest.fixture
def test_user():
    '''Fixture for a creating a test user'''

    user_info = {
        'email': 'test.user@email.com',
        'password': 'password',
        'name_first': 'First',
        'name_last': 'Last'
    }
    register = requests.post(f"{BASE_URL}:{PORT}/auth/register",
                             json=user_info)
    payload = register.json()
    return payload


@pytest.fixture
def invalid_token(test_user):
    '''Fixture for a creating an invalid token'''
    token = test_user['token']
    logout = requests.post(f"{BASE_URL}:{PORT}/auth/register",
                           json={'token': token})
    assert logout['is_success']
    return token


@pytest.fixture
def test_channel(test_user):
    '''Fixture for a creating a test channel'''
    channel_info = {
        'token': test_user['token'],
        'channel_name': 'Channel',
        'is_public': True
    }
    new_channel = requests.post(f"{BASE_URL}:{PORT}/channels/create",
                                json=channel_info)
    payload = new_channel.json()
    return payload


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
        register = requests.post(f"{BASE_URL}:{PORT}/auth/register",
                                 json=user_info)
        payload = register.json()
        return payload

    return _new_user


@pytest.fixture
def make_join_channel():
    '''Factory as a fixture for a test user to create a new channel and joining it'''
    def _make_join_channel(target_user, channel_name):
        channel_info = {
            'token': target_user['token'],
            'channel_name': channel_name,
            'is_public': True
        }
        new_channel = requests.post(f"{BASE_URL}:{PORT}/channels/create",
                                    json=channel_info)
        payload = new_channel.json()
        return payload

    return _make_join_channel


@pytest.fixture
def get_user_profile():
    '''Factory as a fixture for a retrieving user info'''
    def _get_user_profile(token, u_id):
        query_string = urllib.parse.urlencode({'token': token, 'u_id': u_id})
        user_profile = requests.get(f"{BASE_URL}/user/profile?{query_string}")
        payload = user_profile.json()
        return payload

    return _get_user_profile


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