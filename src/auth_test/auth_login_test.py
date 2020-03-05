import pytest
import auth
from error import InputError


@pytest.fixture
def paris():
    '''Fixture for a creating a user named Paris Cler'''

    return auth.auth_register('pariscler@email.com', 'pariscler0229', 'Paris',
                              'Cler')


def test_login_return_type(paris):
    '''Test the types of values returned by auth_login'''

    paris_login = auth.auth_login('pariscler@email.com', 'pariscler0229')
    assert isinstance(paris_login['u_id'], int)
    assert isinstance(paris_login['token'], str)


def test_login_u_id(paris):
    '''Test that the u_id returned auth_login matches u_id returned by auth_register'''

    paris_login = auth.auth_login('pariscler@email.com', 'pariscler0229')
    assert paris_login['u_id'] == paris['u_id']


def test_login_password(paris):
    '''Test auth_login with an incorrect password'''

    # Password is not correct
    with pytest.raises(InputError):
        auth.auth_login('pariscler@email.com', 'incorrect_password')


def test_login_invalid_user():
    '''Test with an email which does not belong to a user'''

    with pytest.raises(InputError):
        auth.auth_login('non_existent_user@email.com', '12345678')


def test_login_multiple_sessions(paris):
    '''Test that auth_login can create multiple session at once'''

    session_1 = auth.auth_login('pariscler@email.com', 'pariscler0229')
    session_2 = auth.auth_login('pariscler@email.com', 'pariscler0229')
    session_3 = auth.auth_login('pariscler@email.com', 'pariscler0229')

    session_tokens = [
        paris['token'], session_1['token'], session_2['token'],
        session_3['token']
    ]

    # Verify that all session_tokens are unique
    assert len(set(session_tokens)) == len(session_tokens)


def test_login_email_valid(valid_emails):
    '''Test input of valid emails into auth_login'''

    for email in valid_emails:
        auth.auth_login(email, 'password')


def test_login_email_invalid(invalid_emails):
    '''Test input of invalid emails into auth_login'''

    for email in invalid_emails:
        with pytest.raises(InputError):
            auth.auth_login(email, 'password')
