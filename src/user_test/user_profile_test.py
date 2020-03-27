import helpers
import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'

# =====================================================
# ========== TESTING USER PROFILE FUNCTION ============
# =====================================================

def test_profile_return_types(reset, new_user, new_channel):
    '''
    Testing the return types of the user_profile function.
    '''

    user = new_user()
    channel = new_channel(user)

    input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', json=input).json()

    assert isinstance(user_info, dict)
    assert isinstance(user_info['u_id'], int)
    assert isinstance(user_info['email'], str)
    assert isinstance(user_info['name_first'], str)
    assert isinstance(user_info['name_last'], str)
    assert isinstance(user_info['handle_str'], str)

def test_profile_u_id(reset, new_user, new_channel):
    '''
    Testing that the u_id in the data_store matches what is returned.
    '''

    user = new_user()
    channel = new_channel(user)

    input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', json=input).json()

    assert user_info['u_id'] == user['u_id']


def test_profile_email(reset, new_user, new_channel):
    '''
    Testing that the email in the data_store matches what is returned.
    '''

    email = 'test@test.com'

    user = new_user(email=email)
    channel = new_channel(user)

    input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', json=input).json()

    user_info_from_data = helpers.get_user(u_id=user['u_id'])

    assert user_info['email'] == user_info_from_data['email']


def test_profile_firstname(reset, new_user, new_channel):
    '''
    Testing that the first name in the data_store matches what is returned.
    '''

    user = new_user()
    channel = new_channel(user)

    input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', json=input).json()

    user_info_from_data = helpers.get_user(u_id=user['u_id'])

    assert user_info['name_first'] == user_info_from_data['name_first']


def test_profile_lastname(reset, new_user, new_channel):
    '''
    Testing that the last name in the data_store matches what is returned.
    '''

    user = new_user()
    channel = new_channel(user)

    input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', json=input).json()

    user_info_from_data = helpers.get_user(u_id=user['u_id'])

    assert user_info['name_last'] == user_info_from_data['name_last']


def test_profile_handle(reset, new_user, new_channel):
    '''
    Testing that the handle in the data_store matches what is returned.
    '''

    user = new_user()
    channel = new_channel(user)

    input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', json=input).json()

    user_info_from_data = helpers.get_user(u_id=user['u_id'])

    assert user_info['handle_str'] == user_info_from_data['handle_str']


def test_profile_no_user(reset, new_user, new_channel):
    '''
    Testing that the function raises an error if the u_id does not exist.
    '''

    user = new_user()
    channel = new_channel(user)

    input = {
        'token': user['token'],
        'u_id': 2
    }
    with pytest.raises(requests.HTTPError):
        user_info = requests.get(f'{BASE_URL}/user/profile', json=input).json()
