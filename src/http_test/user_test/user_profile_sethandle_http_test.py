'''
Testing the functionality of the user_profile_sethandle function.

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

def test_profile_sethandle_return(reset, new_user):
    '''
    Testing the return types of the user_profile_sethandle function.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'handle_str': 'uniquehandle'
    }

    set_handle = requests.put(f'{BASE_URL}/user/profile/sethandle', json=func_input).json()

    assert isinstance(set_handle, dict)
    assert not set_handle


def test_sethandle(reset, new_user):
    '''
    Testing the functionality of updating the user's handle.
    '''

    # ================ SET-UP ===================

    user = new_user(name_first='Jim', name_last='Nottest')

    input_for_profile = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_pre_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_handle = 'jimnottest'

    assert user_pre_info['user']['handle_str'] == expected_handle

    # ================ TESTING ==================

    func_input = {
        'token': user['token'],
        'handle_str': 'uniquehandle'
    }

    requests.put(f'{BASE_URL}/user/profile/sethandle', json=func_input)

    user_post_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_handle = 'uniquehandle'

    assert user_post_info['user']['handle_str'] == expected_handle


def test_changetocurrent(reset, new_user):
    '''
    Testing that changing the handle to the user's current handle will
    return an empty dictionary and not raise an error.
    '''

    # ================ SET-UP ===================

    user = new_user(name_first='Jim', name_last='Nottest')

    input_for_profile = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_pre_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_handle = 'jimnottest'

    assert user_pre_info['user']['handle_str'] == expected_handle

    # ================ TESTING ==================

    func_input = {
        'token': user['token'],
        'handle_str': 'jimnottest'
    }

    set_handle = requests.put(f'{BASE_URL}/user/profile/sethandle', json=func_input).json()

    assert isinstance(set_handle, dict)
    assert not set_handle


def test_handle_toolong(reset, new_user):
    '''
    Testing that trying to change the handle to a length greater than 20
    characters will raise an error.
    '''

    user = new_user(name_first='Jim', name_last='Nottest')

    func_input = {
        'token': user['token'],
        'handle_str': 'i' * 21
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/user/profile/sethandle', json=func_input).raise_for_status()

def test_handle_tooshort(reset, new_user):
    '''
    Testing that trying to change the handle to a length less than 2 characters
    will raise an error.
    '''

    user = new_user(name_first='Jim', name_last='Nottest')

    func_input = {
        'token': user['token'],
        'handle_str': 'i'
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/user/profile/sethandle', json=func_input).raise_for_status()


def test_handle_used(reset, new_user):
    '''
    Testing that trying to change the handle to one that is already being
    used by another user will raise an error.
    '''

    # ================ SET-UP ===================

    user = new_user(name_first='Jim', name_last='Nottest')
    second_user = new_user(email='notused@test.com', name_first='User', name_last='second')

    input_for_profile = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_handle = 'jimnottest'

    # Assert that string expected_handle is being used.
    assert user_info['user']['handle_str'] == expected_handle

    # ================ TESTING ==================

    func_input = {
        'token': second_user['token'],
        'handle_str': 'jimnottest'
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/user/profile/sethandle', json=func_input).raise_for_status()


def test_invalid_token(reset, invalid_token):
    '''
    Testing that an invalid token will raise an error.
    '''

    func_input = {
        'token': invalid_token,
        'handle_str': 'uniquehandle',
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/user/profile/sethandle', json=func_input).raise_for_status()
