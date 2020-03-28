'''Pytest script for testing /auth/login route'''
import requests as req
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_login_return_type(reset, new_user):  # pylint: disable=W0613
    '''Test the types of values returned by auth_login'''

    user_info = {
        'email': 'test@email.com',
        'password': 'password',
    }

    new_user(email=user_info['email'], password=user_info['password'])

    user = req.post(f"{BASE_URL}/auth/login", json=user_info).json()

    assert isinstance(user['u_id'], int)
    assert isinstance(user['token'], str)


def test_login_u_id(reset, new_user):  # pylint: disable=W0613
    '''Test that the u_id returned auth_login matches u_id returned by auth_register'''

    user_info = {
        'email': 'test@email.com',
        'password': 'password',
    }

    register = new_user(email=user_info['email'],
                        password=user_info['password'])

    login = req.post(f"{BASE_URL}/auth/login", json=user_info).json()

    assert register['u_id'] == login['u_id']


def test_login_password(reset, new_user):  # pylint: disable=W0613
    '''Test auth_login with an incorrect password'''

    user_info = {
        'email': 'test@email.com',
        'password': 'incorrect password',  # This is not the correct password
    }

    new_user(email=user_info['email'], password='correct password')

    with pytest.raises(req.HTTPError):
        req.post(f"{BASE_URL}/auth/login", json=user_info).raise_for_status()


def test_login_invalid_user(reset):  # pylint: disable=W0613
    '''Test with an email which does not belong to a user'''

    user_info = {
        'email': 'test@email.com',
        'password': 'password',
    }

    with pytest.raises(req.HTTPError):
        req.post(f"{BASE_URL}/auth/login", json=user_info).raise_for_status()


def test_login_multiple_sessions(reset, new_user):  # pylint: disable=W0613
    '''Test that auth_login can create multiple session at once'''

    user_info = {
        'email': 'test@email.com',
        'password': 'password',
    }

    new_user(email=user_info['email'], password=user_info['password'])

    req.post(f"{BASE_URL}/auth/login", json=user_info).raise_for_status()
    req.post(f"{BASE_URL}/auth/login", json=user_info).raise_for_status()
    req.post(f"{BASE_URL}/auth/login", json=user_info).raise_for_status()


def test_login_unique_token(reset, new_user):  # pylint: disable=W0613
    '''Test that auth_login tokens are unique to the user'''

    user_1 = {'email': 'user1@email.com', 'password': 'password'}
    user_2 = {'email': 'user2@email.com', 'password': 'password'}
    new_user(email=user_1['email'], password=user_1['password'])
    new_user(email=user_2['email'], password=user_2['password'])

    user_1_login = req.post(f"{BASE_URL}/auth/login", json=user_1).json()
    user_2_login = req.post(f"{BASE_URL}/auth/login", json=user_2).json()

    tokens = [user_1_login['token'], user_2_login['token']]

    # Verify that all tokens are unique
    assert len(set(tokens)) == len(tokens)


def test_login_email_valid(reset, valid_emails, new_user):  # pylint: disable=W0613
    '''Test input of valid emails into auth_login'''

    for email in valid_emails:
        new_user(email=email)  # Email must belong to a user

        user_info = {
            'email': email,
            'password': 'password',
        }

        req.post(f"{BASE_URL}/auth/login", json=user_info).raise_for_status()


def test_login_email_invalid(reset, invalid_emails):  # pylint: disable=W0613
    '''Test input of invalid emails into auth_login'''

    for email in invalid_emails:
        # No user was created here.
        # Assume that email checking occurs before checking if email belongs to user

        user_info = {
            'email': email,
            'password': 'password',
        }

        with pytest.raises(req.HTTPError):
            req.post(f"{BASE_URL}/auth/login",
                     json=user_info).raise_for_status()
