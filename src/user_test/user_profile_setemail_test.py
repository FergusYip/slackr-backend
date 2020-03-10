import user
import auth
import pytest
from error import AccessError, InputError

# =====================================================
# ===== TESTING USER PROFILE SET EMAIL FUNCTION =======
# =====================================================

def test_profile_setemail(test_user):

    ''' Testing an average case where a user will change their own email to
    a valid and unique email address. '''

    user.user_profile_setemail(test_user['token'], 'tester2@test.com')
    profile_info = user.user_profile(test_user['token'], test_user['u_id'])

    assert profile_info['user']['email'] == 'tester2@test.com'


def test_profile_setemail_used_by_other_user(test_user, new_user):

    ''' Testing a case where a user attempts to change their email address to
    one that is already in use. '''

    user.user_profile_setemail(test_user['token'], 'test@test.com')

    second_user = new_user('tester@test.com')

    with pytest.raises(InputError):
        user.user_profile_setemail(second_user['token'], 'test@test.com')


def test_profile_setemail_no_change(test_user):

    ''' Testing a case where the user attempts to change their email address
    to their current one. '''

    user.user_profile_setemail(test_user['token'], 'test@test.com')

    with pytest.raises(InputError):
        user.user_profile_setemail(test_user['token'], 'test@test.com')


def test_profile_setemail_invalidtoken(invalid_token):

    ''' Testing a case where an invalid token is input into the function. This
    will result in an AccessError being raised. '''

    with pytest.raises(AccessError):
        user.user_profile_setemail(invalid_token, 'test@test.com')


def test_profile_setemail_valid_emails(test_user, valid_emails):

    ''' Testing the user_profile_setemail function against the pytest fixture
    featuring a tuple of valid emails. '''

    for email in valid_emails:
        user.user_profile_setemail(test_user['token'], email)
        profile_info = user.user_profile(test_user['token'], test_user['u_id'])

        assert profile_info['user']['email'] == email


def test_profile_setemail_invalid_emails(test_user, invalid_emails):

    ''' Testing the user_profile_setemail function against the pytest fixture
    featuring a tuple of invalid emails. '''

    for email in invalid_emails:
        with pytest.raises(InputError):
            user.user_profile_setemail(test_user['token'], email)
