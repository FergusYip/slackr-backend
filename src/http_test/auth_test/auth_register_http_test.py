'''Pytest script for testing /auth/register route'''
import requests as req
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_register_return_type(reset, new_user):  # pylint: disable=W0613
    '''Test the types of values returned by auth_register'''

    user = new_user()
    assert isinstance(user['u_id'], int)
    assert isinstance(user['token'], str)


def test_register_duplicate(reset):  # pylint: disable=W0613
    '''Test the registration of multiple users with the same email'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',
        'name_first': 'Theresa',
        'name_last': 'Vanaria'
    }

    # # Setup 'existing' user
    req.post(f"{BASE_URL}/auth/register", json=user_info)

    with pytest.raises(req.HTTPError):
        req.post(f"{BASE_URL}/auth/register",
                 json=user_info).raise_for_status()


def test_register_valid_password(reset):  # pylint: disable=W0613
    '''Test the input of a valid password length into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',  # Valid
        'name_first': 'Theresa',
        'name_last': 'Vanaria'
    }

    req.post(f"{BASE_URL}/auth/register", json=user_info).raise_for_status()


def test_register_invalid_password(reset):  # pylint: disable=W0613
    '''Test the input of an invalid password length into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': '12345',  # <6 Password Length
        'name_first': 'Theresa',
        'name_last': 'Vanaria'
    }

    with pytest.raises(req.HTTPError):
        req.post(f"{BASE_URL}/auth/register",
                 json=user_info).raise_for_status()


def test_register_long_password(reset):  # pylint: disable=W0613
    '''Test the input of a password with 32 characters into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'i' * 32,
        'name_first': 'Theresa',
        'name_last': 'Vanaria'
    }

    # within the (assumed) maximum length for password
    req.post(f"{BASE_URL}/auth/register", json=user_info).raise_for_status()


def test_register_first_name(reset):  # pylint: disable=W0613
    '''Test the input of a valid first name length into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',
        'name_first': 'Theresa',
        'name_last': 'Vanaria'
    }

    # Valid
    req.post(f"{BASE_URL}/auth/register", json=user_info).raise_for_status()


def test_register_short_first_name(reset):  # pylint: disable=W0613
    '''Test the input of first name that is too short into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',
        'name_first': 'Theresa',
        'name_last': 'Vanaria'
    }

    # <1 Character
    user_info['name_first'] = ''
    with pytest.raises(req.HTTPError):
        req.post(f"{BASE_URL}/auth/register",
                 json=user_info).raise_for_status()


def test_register_long_first_name(reset):  # pylint: disable=W0613
    '''Test the input of first name that is too long into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',
        'name_first': 'i' * 51,  # >50 Characters
        'name_last': 'Vanaria'
    }

    with pytest.raises(req.HTTPError):
        req.post(f"{BASE_URL}/auth/register",
                 json=user_info).raise_for_status()


def test_register_last_name(reset):  # pylint: disable=W0613
    '''Test the input of a valid last name length into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',
        'name_first': 'Theresa',
        'name_last': 'Vanaria'
    }

    # Valid
    req.post(f"{BASE_URL}/auth/register", json=user_info).raise_for_status()


def test_register_short_last_name(reset):  # pylint: disable=W0613
    '''Test the input of last name that is too short into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',
        'name_first': 'Theresa',
        'name_last': ''  # <1 Character
    }

    user_info['name_last'] = ''
    with pytest.raises(req.HTTPError):
        req.post(f"{BASE_URL}/auth/register",
                 json=user_info).raise_for_status()


def test_register_long_last_name(reset):  # pylint: disable=W0613
    '''Test the input of last name that is too long into auth_register'''

    user_info = {
        'email': 'theresavanaria@email.com',
        'password': 'password',
        'name_first': 'Theresa',
        'name_last': 'i' * 51  # >50 Characters
    }

    with pytest.raises(req.HTTPError):
        req.post(f"{BASE_URL}/auth/register",
                 json=user_info).raise_for_status()


def test_register_handle(reset, get_user_profile):  # pylint: disable=W0613
    '''Test that the handle generated by auth_register matches specification'''

    user_info = {
        'email': 'valid@email.com',
        'password': 'password',
        'name_first': 'First',
        'name_last': 'Last'
    }

    user = req.post(f"{BASE_URL}/auth/register", json=user_info).json()
    user_profile = get_user_profile(user['token'], user['u_id'])

    assert user_profile['handle_str'] == 'firstlast'


def test_register_unique_handle(reset, get_user_profile):  # pylint: disable=W0613
    '''Test that handles generated by auth_register are unique'''

    user_info = {
        'password': 'password',
        'name_first': 'Harun',
        'name_last': 'Thomson'
    }

    user_info['email'] = 'user1@email.com'
    user_1 = req.post(f"{BASE_URL}/auth/register", json=user_info).json()

    user_info['email'] = 'user2@email.com'
    user_2 = req.post(f"{BASE_URL}/auth/register", json=user_info).json()

    user_profile_1 = get_user_profile(user_1['token'], user_1['u_id'])
    user_profile_2 = get_user_profile(user_2['token'], user_2['u_id'])

    assert user_profile_1['handle_str'] != user_profile_2['handle_str']


def test_register_long_handle(reset, get_user_profile):  # pylint: disable=W0613
    '''Test that handles generated by auth_register are cut off at 20 characters'''

    user_info = {
        'email': 'valid@email.com',
        'password': 'password',
        'name_first': '123456789testing',
        'name_last': '123456789testing'
    }

    user = req.post(f"{BASE_URL}/auth/register", json=user_info).json()
    user_profile = get_user_profile(user['token'], user['u_id'])

    assert user_profile['handle_str'] == '123456789testing1234'


def test_register_email_valid(reset, valid_emails):  # pylint: disable=W0613
    '''Test input of valid emails into auth_register'''

    for email in valid_emails:
        user_info = {
            'email': email,
            'password': 'password',
            'name_first': 'First',
            'name_last': 'Last'
        }
        req.post(f"{BASE_URL}/auth/register",
                 json=user_info).raise_for_status()


def test_register_email_invalid(reset, invalid_emails):  # pylint: disable=W0613
    '''Test input of invalid emails into auth_register'''

    for email in invalid_emails:

        user_info = {
            'email': email,
            'password': 'password',
            'name_first': 'First',
            'name_last': 'Last'
        }

        with pytest.raises(req.HTTPError):
            req.post(f"{BASE_URL}/auth/register",
                     json=user_info).raise_for_status()
