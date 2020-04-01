'''
Testing the functionality of the user_profile_setname function.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'

# =====================================================
# ========== TESTING USER PROFILE FUNCTION ============
# =====================================================

def test_profile_setname_return(reset, new_user):
    '''
    Testing the return types of the user_profile function.
    '''

    user = new_user(name_first='Jim', name_last='Nottest')

    func_input = {
        'token': user['token'],
        'name_first': 'John',
        'name_last': 'Test'
    }

    set_name = requests.get(f'{BASE_URL}/user/profile', params=func_input).json()

    assert isinstance(set_name, dict)


def test_setfirstname(reset, new_user):
    '''
    Testing the functionality of updating the user's first name.
    '''

    # ================ SET-UP ===================

    user = new_user(name_first='Jim', name_last='Nottest')

    input_for_profile = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_pre_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_firstname = 'Jim'

    assert user_pre_info['name_first'] == expected_firstname

    # ================ TESTING ==================

    func_input = {
        'token': user['token'],
        'name_first': 'John',
        'name_last': 'Test'
    }

    requests.put(f'{BASE_URL}/user/profile/setname', json=func_input).json()

    user_post_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_firstname = 'John'

    assert user_post_info['name_first'] == expected_firstname


def test_setlastname(reset, new_user):
    '''
    Testing the functionality of updating the user's last name.
    '''

    # ================ SET-UP ===================

    user = new_user(name_first='Jim', name_last='Nottest')

    input_for_profile = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_pre_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_lastname = 'Nottest'

    assert user_pre_info['name_last'] == expected_lastname

    # ================ TESTING ==================

    func_input = {
        'token': user['token'],
        'name_first': 'John',
        'name_last': 'Test'
    }

    requests.put(f'{BASE_URL}/user/profile/setname', json=func_input).json()

    user_post_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_lastname = 'Test'

    assert user_post_info['name_last'] == expected_lastname


def test_setboth(reset, new_user):
    '''
    Testing the functionality of updating both the user's first and
    last name.
    '''

    # ================ SET-UP ===================

    user = new_user(name_first='Jim', name_last='Nottest')

    input_for_profile = {
        'token': user['token'],
        'u_id': user['u_id']
    }

    user_pre_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_firstname = 'Jim'
    expected_lastname = 'Nottest'

    assert user_pre_info['name_first'] == expected_firstname
    assert user_pre_info['name_last'] == expected_lastname

    # ================ TESTING ==================

    func_input = {
        'token': user['token'],
        'name_first': 'John',
        'name_last': 'Test'
    }

    requests.put(f'{BASE_URL}/user/profile/setname', json=func_input).json()

    user_post_info = requests.get(f'{BASE_URL}/user/profile', params=input_for_profile).json()
    expected_firstname = 'John'
    expected_lastname = 'Test'

    assert user_post_info['name_first'] == expected_firstname
    assert user_post_info['name_last'] == expected_lastname


def test_invalid_firstname(reset, new_user):
    '''
    Testing that trying to change the first name to something greater than
    50 characters uninclusive, should raise an error.
    '''

    user = new_user(name_first='Jim', name_last='Nottest')

    func_input = {
        'token': user['token'],
        'name_first': 'i' * 51,
        'name_last': 'Test'
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/user/profile/setname', json=func_input).raise_for_status()


def test_invalid_lastname(reset, new_user):
    '''
    Testing that trying to change the last name to something greater than
    50 characters uninclusive, should raise an error.
    '''

    user = new_user(name_first='Jim', name_last='Nottest')

    func_input = {
        'token': user['token'],
        'name_first': 'John',
        'name_last': 'i' * 51
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/user/profile/setname', json=func_input).raise_for_status()


def test_invalid_token(reset, invalid_token):
    '''
    Testing that an invalid token will raise an error.
    '''

    func_input = {
        'token': invalid_token,
        'name_first': 'John',
        'name_last': 'Test'
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/user/profile/setname', json=func_input).raise_for_status()
