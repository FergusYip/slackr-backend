import user
import auth
import pytest
from error import AccessError, InputError

# =====================================================
# ========== TESTING USER PROFILE FUNCTION ============
# =====================================================

def test_averagecase_uid():
    # Storing the new user's information in a variable to check values.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    # Storing the profile information in a variable to check values.
    profile_information = user.user_profile(new_user['token'], new_user['u_id'])
    # Asserting the new user's ID is the same as what is displayed when calling
    # the user_profile function.
    assert(new_user['u_id'] == profile_information['user']['u_id'])

def test_averagecase_email():
    # Storing the new user's information in a variable to check values.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    # Storing the profile information in a variable to check values.
    profile_information = user.user_profile(new_user['token'], new_user['u_id'])
    # Asserting the email returned is the same as the new user.
    assert('test@test.com' == profile_information['user']['email'])

def test_averagecase_firstname():
    # Storing the new user's information in a variable to check values.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    # Storing the profile information in a variable to check values.
    profile_information = user.user_profile(new_user['token'], new_user['u_id'])
    # Asserting the first name returned is the same as the new user.
    assert('Lorem' == profile_information['user']['name_first'])

def test_averagecase_lastname():
    # Storing the new user's information in a variable to check values.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    # Storing the profile information in a variable to check values.
    profile_information = user.user_profile(new_user['token'], new_user['u_id'])
    # Asserting the last name returned is the same as the new user.
    assert('Ipsum' == profile_information['user']['name_last'])

def test_averagecase_handle():
    # Storing the new user's information in a variable to check values.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    # Storing the profile information in a variable to check values.
    profile_information = user.user_profile(new_user['token'], new_user['u_id'])
    # Asserting the handle returned matches the assumptions made about handle
    # generation.
    assert('loremipsum' == profile_information['user']['handle_str'])

def test_invalid_uid():
    # Storing the new user's information in a variable to check values.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    # Assumptions made about u_ids state that 'NOTAUID' is not a valid u_id.
    # Thus, trying to find profile information should raise an InputError.
    with pytest.raises(InputError) as e:
        user.user_profile(new_user['token'], 'NOTAUID')

def invalid_token():
    # Storing the new user's information in a variable to check values.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    with pytest.raises(AccessError) as e:
        user.user_profile('INVALIDTOKEN', new_user['u_id'])

def unauthorized_profile():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    second_user = auth.auth_register('unique@test.com', 'PaSsWoRd1', 'Hello', 'World')
    # Any user should be able to call this command.
    user.user_profile(second_user['token'], new_user['u_id'])
