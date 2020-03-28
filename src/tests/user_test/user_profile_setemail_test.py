'''
System testing the user_profile_setemail functionality.
'''

import pytest
import user
from error import AccessError, InputError

# =====================================================
# ===== TESTING USER PROFILE SET EMAIL FUNCTION =======
# =====================================================

def test_setemail_return(reset, test_user): # pylint: disable=W0613
    '''
    Testing the return type of the setemail function.
    '''

    return_type = user.user_profile_setemail(test_user['token'], 'new@test.com')
    assert not return_type
    assert isinstance(return_type, dict)


def test_profile_setemail(reset, test_user): # pylint: disable=W0613
    '''
    Testing an average case where a user will change their own email to
    a valid and unique email address.
    '''

    user.user_profile_setemail(test_user['token'], 'tester@test.com')
    profile_info = user.user_profile(test_user['token'], test_user['u_id'])

    assert profile_info['email'] == 'tester@test.com'


def test_profile_setemail_used_by_other_user(reset, test_user, new_user): # pylint: disable=W0613
    '''
    Testing a case where a user attempts to change their email address to
    one that is already in use.
    '''

    user.user_profile_setemail(test_user['token'], 'test@test.com')

    second_user = new_user('tester@test.com')

    with pytest.raises(InputError):
        user.user_profile_setemail(second_user['token'], 'test@test.com')


def test_profile_setemail_no_change(reset, test_user): # pylint: disable=W0613
    '''
    Testing a case where the user attempts to change their email address
    to their current one.
    '''

    return_type = user.user_profile_setemail(test_user['token'], 'test@test.com')

    # Assert the function returns an empty dictionary.
    assert not return_type
    assert isinstance(return_type, dict)


def test_profile_setemail_invalidtoken(reset, invalid_token): # pylint: disable=W0613
    '''
    Testing a case where an invalid token is input into the function. This
    will result in an AccessError being raised.
    '''

    with pytest.raises(AccessError):
        user.user_profile_setemail(invalid_token, 'test@test.com')


def test_profile_setemail_valid_emails(reset, test_user, valid_emails): # pylint: disable=W0613
    '''
    Testing the user_profile_setemail function against the pytest fixture
    featuring a tuple of valid emails.
    '''

    for email in valid_emails:
        user.user_profile_setemail(test_user['token'], email)
        profile_info = user.user_profile(test_user['token'], test_user['u_id'])

        assert profile_info['email'] == email


def test_profile_setemail_invalid_emails(reset, test_user, invalid_emails): # pylint: disable=W0613
    '''
    Testing the user_profile_setemail function against the pytest fixture
    featuring a tuple of invalid emails.
    '''

    for email in invalid_emails:
        with pytest.raises(InputError):
            user.user_profile_setemail(test_user['token'], email)
