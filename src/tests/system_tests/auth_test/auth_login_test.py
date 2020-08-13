''' System tests for auth_login'''
import pytest
import auth
from error import InputError


def test_login_return_type(reset, new_user):  # pylint: disable=W0613
    '''Test the types of values returned by auth_login'''
    new_user(email='hello@world.com', password='pythonIsKool')
    user_login = auth.auth_login('hello@world.com', 'pythonIsKool')
    assert isinstance(user_login['u_id'], int)
    assert isinstance(user_login['token'], str)


def test_login_u_id(reset, new_user):  # pylint: disable=W0613
    '''Test that the u_id returned auth_login matches u_id returned by auth_register'''
    user = new_user(email='hello@world.com', password='pythonIsKool')
    user_login = auth.auth_login('hello@world.com', 'pythonIsKool')
    assert user_login['u_id'] == user['u_id']


def test_login_password(reset, new_user):  # pylint: disable=W0613
    '''Test auth_login with an incorrect password'''

    new_user(email='hello@world.com', password='pythonIsKool')

    # Password is not correct
    with pytest.raises(InputError):
        auth.auth_login('hello@world.com', 'pythonSucks')


def test_login_invalid_user(reset):  # pylint: disable=W0613
    '''Test with an email which does not belong to a user'''

    with pytest.raises(InputError):
        auth.auth_login('non_existent_user@email.com', '12345678')


def test_login_multiple_sessions(reset, new_user):  # pylint: disable=W0613
    '''Test that auth_login can create multiple session at once'''

    new_user(email='hello@world.com', password='pythonIsKool')
    auth.auth_login('hello@world.com', 'pythonIsKool')
    auth.auth_login('hello@world.com', 'pythonIsKool')
    auth.auth_login('hello@world.com', 'pythonIsKool')


def test_login_unique_token(reset, new_user):  # pylint: disable=W0613
    '''Test that auth_login tokens are unique to the user'''
    new_user(email='user_1@email.com', password='password')
    new_user(email='user_2@email.com', password='password')

    user_1_login = auth.auth_login('user_1@email.com', 'password')
    user_2_login = auth.auth_login('user_2@email.com', 'password')

    tokens = [user_1_login['token'], user_2_login['token']]

    # Verify that all tokens are unique
    assert len(set(tokens)) == len(tokens)


def test_login_email_valid(reset, valid_emails, new_user):  # pylint: disable=W0613
    '''Test input of valid emails into auth_login'''

    for email in valid_emails:
        new_user(email=email)  # Email must belong to a user
        auth.auth_login(email, 'password')


def test_login_email_invalid(reset, invalid_emails):  # pylint: disable=W0613
    '''Test input of invalid emails into auth_login'''

    for email in invalid_emails:
        # No user was created here.
        # Assume that email checking occurs before checking if email belongs to user

        with pytest.raises(InputError):
            auth.auth_login(email, 'password')


def test_login_insufficient_params(reset):  # pylint: disable=W0613
    '''Test input of invalid parameters into auth_login'''

    with pytest.raises(InputError):
        auth.auth_login(None, None)
