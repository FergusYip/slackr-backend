import json
import requests
import urllib
import pytest
# import auth
# import user
from error import AccessError, InputError

BASE_URL = 'http://127.0.0.1:8080'


def test_register_return_type(new_user, reset):
    '''Test the types of values returned by auth_register'''

    user = new_user()
    assert isinstance(user['u_id'], int)
    assert isinstance(user['token'], str)


def test_register_duplicate(reset):
    '''Test the registration of multiple users with the same email'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',
        'name_first': 'Theresa',
        'name_last': 'Vanaria'
    }

    # # Setup 'existing' user
    requests.post(f"{BASE_URL}/auth/register", json=user_info)

    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register", json=user_info)


def test_register_password(reset):
    '''Test the input of various password lengths into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',
        'name_first': 'Theresa',
        'name_last': 'Vanaria'
    }

    # Valid
    requests.post(f"{BASE_URL}/auth/register", json=user_info)

    # <6 Password Length
    user_info['password'] = '12345'
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register", json=user_info)

    # 32 character password that is within the (assumed) maximum length for password
    user_info['password'] = 'i' * 32
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register", json=user_info)


def test_register_first_name(reset):
    '''Test the input of various first name lengths into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',
        'name_first': 'Theresa',
        'name_last': 'Vanaria'
    }

    # Valid
    requests.post(f"{BASE_URL}/auth/register", json=user_info)

    # <1 Character
    user_info['name_first'] = ''
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register", json=user_info)

    # >50 Characters
    user_info['name_first'] = 'i' * 51
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register", json=user_info)


def test_register_last_name(reset):
    '''Test the input of various last name lengths into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',
        'name_first': 'Theresa',
        'name_last': 'Vanaria'
    }

    # Valid
    requests.post(f"{BASE_URL}/auth/register", json=user_info)

    # <1 Character
    user_info['name_last'] = ''
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register", json=user_info)

    # >50 Characters
    user_info['name_last'] = 'i' * 51
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/register", json=user_info)


def test_register_handle(new_user, get_user_profile, reset):
    '''Test that the handle generated by auth_register matches assumption'''

    user = new_user(name_first='First', name_last='Last')
    user_profile = get_user_profile(user['token'], user['u_id'])

    assert user_profile['handle_str'] == 'firstlast'


def test_register_unique_handle(new_user, get_user_profile, reset):
    '''Test that handles generated by auth_register are unique'''

    user_1 = new_user('valid1@email.com')
    user_profile_1 = get_user_profile(user_1['token'], user_1['u_id'])

    user_2 = new_user('valid2@email.com')
    user_profile_2 = get_user_profile(user_2['token'], user_2['u_id'])

    assert user_profile_1['user']['handle_str'] != user_profile_2['user'][
        'handle_str']


def test_register_long_handle(new_user, get_user_profile, reset):
    '''Test that handles generated by auth_register are cut off at 20 characters'''

    user = new_user('valid@email.com', 'password', '123456789testing',
                    '123456789testing')
    user_profile = get_user_profile(user['token'], user['u_id'])
    assert user_profile['user']['handle_str'] == '123456789testing1234'


def test_register_email_valid(valid_emails, new_user, reset):
    '''Test input of valid emails into auth_register'''

    for email in valid_emails:
        new_user(email)


def test_register_email_invalid(invalid_emails, new_user, reset):
    '''Test input of invalid emails into auth_register'''

    for email in invalid_emails:
        with pytest.raises(InputError):
            new_user(email)
