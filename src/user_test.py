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

# =====================================================
# ====== TESTING USER PROFILE SETNAME FUNCTION ========
# =====================================================

def test_averagecase_setname():
    # Creating a user and calling user_profile_setname without raising an error.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    user.user_profile_setname(new_user['token'], 'Ipsum', 'Lorem')

def test_firstzerocharacter():
    # Creating a user and changing their first name to be 0 characters. Thus,
    # raising an InputError as this is invalid.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    with pytest.raises(InputError) as e:
        user.user_profile_setname(new_user['token'], '', 'Lorem')

def test_firstoverfifty():
    # Creating a user and chaning thier first name to be over 50 characters.
    # Thus, raising an InputError.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    with pytest.raises(InputError) as e:
        user.user_profile_setname(new_user['token'], 'i' * 51, 'Lorem')

def test_lastzerocharacter():
    # Creating a user and changing their last name to be 0 characters. Thus,
    # raising an InputError.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    with pytest.raises(InputError) as e:
        user.user_profile_setname(new_user['token'], 'Ipsum', '')

def test_lastoverfifty():
    # Creating a user and changing their last name to be over 50 characters.
    # Thus, raising an InputError.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    with pytest.raises(InputError) as e:
        user.user_profile_setname(new_user['token'], 'Ipsum', 'i' * 50)

'''Possible testing of invalid token. I.e. if a second user tries to change
the target user's name without being authorized. AccessError?'''
