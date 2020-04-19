'''
System tests for the user_profile_sethandle function.
'''

import pytest
import user
from error import AccessError, InputError

# =====================================================
# ===== TESTING USER PROFILE SET HANDLE FUNCTION ======
# =====================================================

def test_profile_sethandle(reset, test_user):
    '''
    Average case test where a user will change their handle to a different
    valid handle.
    '''

    user.user_profile_sethandle(test_user['token'], 'knownhandle')
    profile_info = user.user_profile(test_user['token'], test_user['u_id'])

    assert profile_info['user']['handle_str'] == 'knownhandle'


def test_profile_sethandle_below_char_limit(reset, test_user):
    '''
    Case where a handle change should result in an InputError if the new
    handle is fewer than 2 characters (2 not inclusive).
    '''

    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user['token'], 'i' * 1)


def test_profile_sethandle_above_char_limit(reset, test_user):
    '''
    Case where a handle change should result in an InputError if the new
    handle is greater than 20 characters (20 not inclusive).
    '''

    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user['token'], 'i' * 21)


def test_profile_sethandle_spaces(reset, test_user):
    '''
    Case where a handle change should result in an InputError if the new
    handle contains spaces.
    '''

    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user['token'], 'hello world')


def test_profile_sethandle_existing_handle(reset, test_user, new_user):
    '''
    Case where a user attempts to change their handle to an existing handle.
    '''

    user2 = new_user('tester2@mail.com')
    user.user_profile_sethandle(user2['token'], 'knownhandle')

    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user['token'], 'knownhandle')


def test_profile_sethandle_no_change(reset, test_user):
    '''
    Case where a user attempts to change their handle to their current handle.
    '''

    user.user_profile_sethandle(test_user['token'], 'knownhandle')
    return_type = user.user_profile_sethandle(test_user['token'], 'knownhandle')

    # Assert the function returns an empty dictionary.
    assert not return_type
    assert isinstance(return_type, dict)


def test_profile_sethandle_invalidtoken(reset, invalid_token):
    '''
    Case where an invalid token is passed into the function.
    '''

    with pytest.raises(AccessError):
        user.user_profile_sethandle(invalid_token, 'knownhandle')
