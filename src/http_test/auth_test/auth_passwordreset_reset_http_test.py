'''Pytest script for testing /auth/passwordreset/reset'''
import time
import requests
import pytest
from .read_email_helper import get_msg_from_chunts, delete_all_emails

BASE_URL = 'http://127.0.0.1:8080'


def test_reset_password_input_error(reset):
    '''Test that password reset raises an error when the code is invalid'''
    invalid_reset_code = -1  # Assume that negative codes are invalid

    reset_input = {
        'reset_code': invalid_reset_code,
        'new_password': 'password'
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/auth/passwordreset/reset',
                      json=reset_input).raise_for_status()


def test_reset_password_insufficient_params(reset):
    '''Test that password reset raises an error when insufficient parameters are passed in'''

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/auth/passwordreset/reset',
                      json={}).raise_for_status()


def test_reset_password_short(reset, new_user):
    '''Test password reset with a password that is too short'''

    email = 'thechunts.slackr@gmail.com'
    new_user(email=email, password='pythonIsKool')

    delete_all_emails()

    request_input = {'email': email}

    requests.post(f'{BASE_URL}/auth/passwordreset/request', json=request_input)

    time.sleep(10)

    msg = get_msg_from_chunts()

    latest = msg[0].as_string()

    target_str = 'Your password reset code is '
    code_index = latest.rfind(target_str) + len(target_str)

    code_digits = 6
    code = latest[code_index:code_index + code_digits]

    reset_input = {'reset_code': code, 'new_password': '12345'}

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/auth/passwordreset/reset',
                      json=reset_input).raise_for_status()

    delete_all_emails()


def test_reset_password_valid(reset, new_user):
    '''Test password reset with correct parameters'''
    email = 'thechunts.slackr@gmail.com'
    old_password = 'password'
    new_user(email=email, password=old_password)

    delete_all_emails()

    request_input = {'email': email}

    requests.post(f'{BASE_URL}/auth/passwordreset/request', json=request_input)

    time.sleep(10)

    msg = get_msg_from_chunts()

    latest = msg[0].as_string()

    target_str = 'Your password reset code is '
    code_index = latest.rfind(target_str) + len(target_str)

    code_digits = 6
    code = latest[code_index:code_index + code_digits]

    new_password = '12345678'

    reset_input = {'reset_code': code, 'new_password': new_password}

    requests.post(f'{BASE_URL}/auth/passwordreset/reset',
                  json=reset_input).raise_for_status()

    login_input = {'email': email, 'password': new_password}
    requests.post(f'{BASE_URL}/auth/login',
                  json=login_input).raise_for_status()

    login_input['password'] = old_password

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/auth/login',
                      json=login_input).raise_for_status()

    delete_all_emails()
