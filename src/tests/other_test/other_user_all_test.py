import pytest
import other
import user
from error import AccessError


def test_users_all_single_user(test_user):
    '''Test that a single user profile is returned by user_all'''

    test_user_profile = user.user_profile(test_user['token'],
                                          test_user['u_id'])['user']
    all_users = other.users_all(test_user['token'])

    assert test_user_profile in all_users['users']


def test_users_all_multiple_users(new_user):
    '''Test that user_all returns the number of registered users'''

    user_1 = new_user('user_1@email.com')
    assert len(other.users_all(user_1['token'])['users']) == 1

    user_2 = new_user('user_2@email.com')
    assert len(other.users_all(user_2['token'])['users']) == 2

    user_3 = new_user('user_3@email.com')
    assert len(other.users_all(user_3['token'])['users']) == 3


def test_users_all_invalid_token(invalid_token):
    '''Test user_all with invalid token'''

    with pytest.raises(AccessError):
        other.users_all(invalid_token)
