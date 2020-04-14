'''
Testing the functionality of the user_profile function.

Parameters used:
    reset: Reset is a function defined in conftest.py that restores all values
           in the data_store back to being empty.
    new_user: A function defined in conftest.py that will create a new user based on
              default values that can be specified. Returns the u_id and token.
    invalid_token: A function defined in conftest.py that creates a new user, stores the
                   token, and logs the user out. It will then return this invalid token.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'

# =====================================================
# ========== TESTING USER PROFILE FUNCTION ============
# =====================================================

def test_profile_return_types(reset, new_user):
    '''
    Testing the return types of the user_profile function.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', params=func_input).json()

    assert isinstance(user_info, dict)
    assert isinstance(user_info['user'], dict)
    assert isinstance(user_info['user']['u_id'], int)
    assert isinstance(user_info['user']['email'], str)
    assert isinstance(user_info['user']['name_first'], str)
    assert isinstance(user_info['user']['name_last'], str)
    assert isinstance(user_info['user']['handle_str'], str)

def test_profile_u_id(reset, new_user):
    '''
    Testing that the u_id in the data_store matches what is returned.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', params=func_input).json()

    assert user_info['user']['u_id'] == user['u_id']


def test_profile_email(reset, new_user):
    '''
    Testing that the email in the data_store matches what is returned.
    '''

    email = 'test@test.com'
    user = new_user(email=email)

    func_input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', params=func_input).json()

    assert user_info['user']['email'] == email


def test_profile_firstname(reset, new_user):
    '''
    Testing that the first name in the data_store matches what is returned.
    '''

    first_name = 'John'
    user = new_user(name_first=first_name)

    func_input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', params=func_input).json()

    assert user_info['user']['name_first'] == first_name


def test_profile_lastname(reset, new_user):
    '''
    Testing that the last name in the data_store matches what is returned.
    '''

    last_name = 'Test'
    user = new_user(name_last=last_name)

    func_input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', params=func_input).json()

    assert user_info['user']['name_last'] == last_name


def test_profile_handle(reset, new_user):
    '''
    Testing that the handle in the data_store matches what is returned.
    '''

    user = new_user(name_first='John', name_last='Test')

    func_input = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', params=func_input).json()

    # Lowercase concatenation of the first and last name of the user.
    handle_expected = 'johntest'

    assert user_info['user']['handle_str'] == handle_expected


def test_profile_no_user(reset, new_user):
    '''
    Testing that the function raises an error if the u_id does not exist.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'u_id': 2
    }
    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/user/profile', params=func_input).raise_for_status()


def test_invalid_token(reset, invalid_token):
    '''
    Testing that an invalid token will raise an error.
    '''

    func_input = {
        'token': invalid_token,
        'u_id': 1,
    }

    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/user/profile', params=func_input).raise_for_status()
