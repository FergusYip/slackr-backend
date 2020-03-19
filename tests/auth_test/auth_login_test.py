import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_login_return_type(new_user, reset):
    '''Test the types of values returned by auth_login'''

    user_info = {
        'email': 'test@email.com',
        'password': 'password',
    }

    new_user(email=user_info['email'], password=user_info['password'])

    user = requests.post(f"{BASE_URL}/auth/login", json=user_info).json()

    assert isinstance(user['u_id'], int)
    assert isinstance(user['token'], str)


def test_login_u_id(new_user, reset):
    '''Test that the u_id returned auth_login matches u_id returned by auth_register'''

    user_info = {
        'email': 'test@email.com',
        'password': 'password',
    }

    register = new_user(email=user_info['email'],
                        password=user_info['password'])

    login = requests.post(f"{BASE_URL}/auth/login", json=user_info).json()

    assert register['u_id'] == login['u_id']


def test_login_password(new_user, reset):
    '''Test auth_login with an incorrect password'''

    user_info = {
        'email': 'test@email.com',
        'password': 'incorrect password',  # This is not the correct password
    }

    new_user(email=user_info['email'], password='correct password')

    # Password is not correct
    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/login", json=user_info).json()


def test_login_invalid_user(reset):
    '''Test with an email which does not belong to a user'''

    user_info = {
        'email': 'test@email.com',
        'password': 'password',
    }

    with pytest.raises(InputError):
        requests.post(f"{BASE_URL}/auth/login", json=user_info).json()


def test_login_multiple_sessions(new_user):
    '''Test that auth_login can create multiple session at once'''

    user_info = {
        'email': 'test@email.com',
        'password': 'password',
    }

    new_user(email=user_info['email'], password=user_info['password'])

    session_1 = requests.post(f"{BASE_URL}/auth/login", json=user_info).json()
    session_2 = requests.post(f"{BASE_URL}/auth/login", json=user_info).json()
    session_3 = requests.post(f"{BASE_URL}/auth/login", json=user_info).json()

    session_tokens = [
        session_1['token'], session_2['token'], session_3['token']
    ]

    # Verify that all session_tokens are unique
    assert len(set(session_tokens)) == len(session_tokens)


def test_login_email_valid(valid_emails):
    '''Test input of valid emails into auth_login'''

    user_info = {
        'email': None,
        'password': 'password',
    }

    for email in valid_emails:
        user_info['email'] = email
        requests.post(f"{BASE_URL}/auth/login", json=user_info).json()


def test_login_email_invalid(invalid_emails):
    '''Test input of invalid emails into auth_login'''

    user_info = {
        'email': None,
        'password': 'password',
    }

    for email in invalid_emails:
        user_info['email'] = email
        requests.post(f"{BASE_URL}/auth/login", json=user_info).json()
