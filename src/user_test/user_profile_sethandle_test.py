import user
import auth
import pytest
from error import AccessError, InputError

# =====================================================
# ===== TESTING USER PROFILE SET HANDLE FUNCTION ======
# =====================================================

def test_averagecase_handle(test_user):

    ''' Average case test where a user will change their handle to a different
    valid handle. '''

    user.user_profile_sethandle(test_user['token'], 'testeraccount42')
    profile_info = user.user_profile(test_user['token'], test_user['u_id'])

    assert profile_info['user']['handle_str'] == 'testeraccount42'


def test_lessthanthree_handle(test_user):

    ''' Case where a handle change should result in an InputError if the new
    handle is fewer than 3 characters (3 not inclusive). '''

    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user['token'], 'i' * 2)


def test_greaterthantwenty_handle(test_user):

    ''' Case where a handle change should result in an InputError if the new
    handle is greater than 20 characters (20 not inclusive). '''

    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user['token'], 'i' * 21)


def test_existing_handle(test_user, new_user):

    ''' Case where a user attempts to change their handle to an existing handle. '''

    user2 = new_user('tester2@mail.com')
    user.user_profile_sethandle(user2['token'], 'knownhandle')

    ''' With a state set at which we are certain user2 has handle 'knownhandle',
    an InputError should be raised when test_user attempts to change their handle
    to 'knownhandle' '''

    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user['token'], 'knownhandle')


def test_changetoitsown(test_user):

    ''' Case where a user attempts to change their handle to their current handle. '''

    user.user_profile_sethandle(test_user['token'], 'knownhandle')

    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user['token'], 'knownhandle')


def test_invalidtoken_handle(test_user):

    ''' Case where an invalid token is passed into the function. '''

    with pytest.raises(AccessError):
        user.user_profile_sethandle('NOTAVALIDTOKEN', 'knownhandle')
