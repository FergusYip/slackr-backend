'''
System tests for the user_profile functionality.
'''

import pytest
import user
import auth
from error import AccessError, InputError

# =====================================================
# ========== TESTING USER PROFILE FUNCTION ============
# =====================================================

def test_averagecase_uid(reset, test_user): # pylint: disable=W0613
    '''
    Testing an average case where a user will request profile information
    about themselves.
    '''

    profile_information = user.user_profile(test_user['token'], test_user['u_id'])

    assert test_user['u_id'] == profile_information['u_id']

def test_averagecase_otheruser(reset, test_user, new_user): # pylint: disable=W0613
    '''
    Testing an average case where a user will request profile information
    about another user.
    '''

    user2 = new_user('tester2@test.com')

    profile_information = user.user_profile(test_user['token'], user2['u_id'])

    assert user2['u_id'] == profile_information['u_id']


def test_averagecase_email(reset, test_user): # pylint: disable=W0613
    '''
    Testing that the user_profile function returns the correct email.
    '''

    user.user_profile_setemail(test_user['token'], 'test@test.com')
    profile_information = user.user_profile(test_user['token'], test_user['u_id'])

    assert  profile_information['email'] == 'test@test.com'


def test_averagecase_firstname(reset, test_user): # pylint: disable=W0613
    '''
    Testing that the user_profile function returns the correct first name.
    '''

    user.user_profile_setname(test_user['token'], 'Lorem', 'Ipsum')
    profile_information = user.user_profile(test_user['token'], test_user['u_id'])

    assert profile_information['name_first'] == 'Lorem'


def test_averagecase_lastname(reset, test_user): # pylint: disable=W0613
    '''
    Testing that the user_profile function returns the correct last name.
    '''

    user.user_profile_setname(test_user['token'], 'Lorem', 'Ipsum')
    profile_information = user.user_profile(test_user['token'], test_user['u_id'])

    assert profile_information['name_last'] == 'Ipsum'


def test_averagecase_handle(reset, test_user): # pylint: disable=W0613
    '''
    Testing that the user_profile function returns the correct handle.
    '''

    user.user_profile_sethandle(test_user['token'], 'testhandle')
    profile_information = user.user_profile(test_user['token'], test_user['u_id'])

    assert profile_information['handle_str'] == 'testhandle'


def test_invalid_uid(reset, test_user): # pylint: disable=W0613
    '''
    Testing the user_profile function if an incorrect u_id is input.
    '''

    with pytest.raises(InputError):
        user.user_profile(test_user['token'], -1)


def test_invalid_token(reset, test_user): # pylint: disable=W0613
    '''
    Testing that the user_profile function if an invalid token is input.
    '''

    assert auth.auth_logout(test_user['token'])['is_success']

    with pytest.raises(AccessError):
        user.user_profile(test_user['token'], test_user['u_id'])
