import user
import auth
import pytest
from error import AccessError, InputError

# =====================================================
# ========== TESTING USER PROFILE FUNCTION ============
# =====================================================

def test_averagecase_uid(test_user):

    ''' Testing an average case where a user will request profile information
    about themselves. '''

    profile_information = user.user_profile(test_user['token'], test_user['u_id'])

    assert test_user['u_id'] == profile_information['user']['u_id']

def test_averagecase_otheruser(test_user, new_user):

    ''' Testing an average case where a user will request profile information
    about another user. '''

    user2 = new_user('tester2@test.com')

    profile_information = user.user_profile(test_user['token'], user2['u_id'])

    assert user2['u_id'] == profile_information['user']['u_id']


def test_averagecase_email(test_user):

    ''' Testing that the user_profile function returns the correct email. '''

    user.user_profile_setemail(test_user['token'], 'test@test.com')
    profile_information = user.user_profile(test_user['token'], test_user['u_id'])

    assert 'test@test.com' == profile_information['user']['email']


def test_averagecase_firstname(test_user):

    ''' Testing that the user_profile function returns the correct first name. '''

    user.user_profile_setname(test_user['token'], 'Lorem', 'Ipsum')
    profile_information = user.user_profile(test_user['token'], test_user['u_id'])

    assert 'Lorem' == profile_information['user']['name_first']


def test_averagecase_lastname(test_user):

    ''' Testing that the user_profile function returns the correct last name. '''

    user.user_profile_setname(test_user['token'], 'Lorem', 'Ipsum')
    profile_information = user.user_profile(test_user['token'], test_user['u_id'])

    assert 'Ipsum' == profile_information['user']['name_last']


def test_averagecase_handle(test_user):

    ''' Testing that the user_profile function returns the correct handle. '''

    user.user_profile_sethandle(test_user['token'], 'testhandle')
    profile_information = user.user_profile(test_user['token'], test_user['u_id'])

    assert 'testhandle' == profile_information['user']['handle_str']


def test_invalid_uid(test_user):

    ''' Testing the user_profile function if an incorrect u_id is input. '''

    with pytest.raises(InputError):
        user.user_profile(test_user['token'], 99999)


def invalid_token(test_user):

    ''' Testing that the user_profile function if an invalid token is input. '''

    with pytest.raises(AccessError):
        user.user_profile('NOTAVALIDTOKEN', test_user['u_id'])
