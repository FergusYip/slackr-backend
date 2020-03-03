import pytest
import auth


@pytest.fixture
def test_user():
    return auth.auth_register('test.user@email.com', 'password', 'First',
                              'Last')


@pytest.fixture
def invalid_token(test_user):
    assert auth.auth_logout(test_user['token'])
    return test_user['token']
