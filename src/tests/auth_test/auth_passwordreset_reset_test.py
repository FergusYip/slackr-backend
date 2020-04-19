''' System tests for auth_passwordreset_reset'''
import time
import pytest
import auth
from error import InputError
from .read_email_helper import get_msg_from_chunts, delete_all_emails


def test_reset_password_input_error(reset):
    '''Test that password reset raises an error when the code is invalid'''
    invalid_reset_code = -1  # Assume that negative codes are invalid
    with pytest.raises(InputError):
        auth.auth_passwordreset_reset(invalid_reset_code, 'pythonIsNotKool')


def test_reset_password_insufficient_params(reset):
    '''Test that password reset raises an error when insufficient parameters are passed in'''

    with pytest.raises(InputError):
        auth.auth_passwordreset_reset(None, None)


def test_reset_password_short(reset, new_user):
    '''Test password reset with a password that is too short'''

    email = 'thechunts.slackr@gmail.com'
    new_user(email=email, password='pythonIsKool')

    delete_all_emails()
    auth.auth_passwordreset_request(email)
    time.sleep(10)

    msg = get_msg_from_chunts()

    latest = msg[0].as_string()

    target_str = 'Your password reset code is '
    code_index = latest.rfind(target_str) + len(target_str)

    code_digits = 6
    code = latest[code_index:code_index + code_digits]

    with pytest.raises(InputError):
        auth.auth_passwordreset_reset(code, '12345')

    delete_all_emails()


def test_reset_password_valid(reset, new_user):
    '''Test password reset with correct parameters'''
    email = 'thechunts.slackr@gmail.com'
    old_password = 'password'
    new_user(email=email, password=old_password)

    delete_all_emails()
    auth.auth_passwordreset_request(email)
    time.sleep(10)

    msg = get_msg_from_chunts()

    latest = msg[0].as_string()

    target_str = 'Your password reset code is '
    code_index = latest.rfind(target_str) + len(target_str)

    code_digits = 6
    code = latest[code_index:code_index + code_digits]

    new_password = '12345678'
    auth.auth_passwordreset_reset(code, new_password)

    auth.auth_login(email, new_password)

    # Logging in with the old password will result in an error
    with pytest.raises(InputError):
        auth.auth_login(email, old_password)

    delete_all_emails()
