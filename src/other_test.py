import pytest
import auth
import other
import user
from error import AccessError


def test_users_all(test_user):
    test_user_profile = user.user_profile(test_user['token'],
                                          test_user['u_id'])['user']
    all_users = other.users_all(test_user['token'])

    assert test_user_profile in all_users['users']


def test_users_all_invalid_token(invalid_token):
    with pytest.raises(AccessError):
        other.users_all(invalid_token)


def test_search_invalid_token(invalid_token):
    with pytest.raises(AccessError):
        other.search(invalid_token, '')
