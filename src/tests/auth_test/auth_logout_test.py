import pytest
import auth
from error import InputError, AccessError


@pytest.fixture
def paris():
    '''Fixture for a creating a user named Paris Cler'''

    return auth.auth_register('pariscler@email.com', 'pariscler0229', 'Paris',
                              'Cler')


def test_logout(paris):
    '''Test that auth_logout returns True on successful Logout'''

    assert auth.auth_logout(paris['token'])['is_success']


def test_logout_invalid_token(invalid_token):
    '''Test that auth_logout raises an AccessError when given invalid token'''

    with pytest.raises(AccessError):
        auth.auth_logout(invalid_token)['is_success']
