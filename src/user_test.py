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

# =====================================================
# ====== TESTING USER PROFILE SETNAME FUNCTION ========
# =====================================================

def test_averagecase_setname():
    # Creating a user and calling user_profile_setname without raising an error.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    user.user_profile_setname(new_user['token'], 'Ipsum', 'Lorem')
    profile_info = user.user_profile(new_user['token'], new_user['u_id'])
    assert profile_info['name_first'] == 'Ipsum'

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

def invalidtoken_namechange():
    # Function to raise an AccessError if the token passed is invalid.
    with pytest.raises(AccessError) as e:
        user.user_profile_setname('INVALIDTOKEN', 'Johnny', 'McJohnny')

# =====================================================
# ===== TESTING USER PROFILE SET EMAIL FUNCTION =======
# =====================================================

def averagecase_email_change():
    # Standard case of a user changing their email address.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    user.user_profile_setemail(new_user['token'], 'unique42@hemail.com')
    profile_info = user.user_profile(new_user['token'], new_user['u_id'])
    assert profile_info['email'] == 'unique42@hemail.com'

def already_used_emailchange():
    # Case where a user already exists with that email address.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    second_user = auth.auth_register('tester@test.com', 'PaSsWoRd1', 'Unique', 'Name')
    with pytest.raises(InputError) as e:
        user.user_profile_setemail(second_user['token'], 'test@test.com')

def no_change_email():
    # Case where the user tries to change their email address to the current one.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    with pytest.raises(InputError) as e:
        user.user_profile_setemail(new_user['token'], 'test@test.com')

def invalidtoken_emailchange():
    # Function to raise an AccessError if the token passed is invalid.
    with pytest.raises(AccessError) as e:
        user.user_profile_setemail('INVALIDTOKEN', 'doesntmatter@gmail.com')

# Valid emails tuple created by Fergus Yip
@pytest.fixture
def valid_emails():
    '''Fixture for a tuple of valid emails'''

    return ('latonyaDAVISON@email.com', '123456789@email.com',
            'lantonyDAVISON123@email.com', 'lantony_davison@email.com',
            'lantony.davison@email.com', 'lantony-davison@email.com')

# Invalid emails tuple created by Fergus Yip
@pytest.fixture
def invalid_emails():
    '''Fixture for a tuple of invalid emails'''

    return (
        '.latonyadavison@email.com',
        'latonyadavison.@email.com',
        'latonya..davison.@email.com',
        'latonya@davison@email.com',
        'latonyadavison.com',
    )

def test_validemailchange(valid_emails):
    # Testing the change to a variety of valid email types.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    for email in valid_emails:
        user.user_profile_setemail(new_user['token'], email)
        profile_info = user.user_profile(new_user['token'], new_user['u_id'])
        assert profile_info['email'] == email

def test_invalidemailchange(invalid_emails):
    # Testing the change to a variety of invalid email types.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    for email in invalid_emails:
        with pytest.raises(InputError) as e:
            user.user_profile_setemail(new_user['token'], email)

# =====================================================
# ===== TESTING USER PROFILE SET HANDLE FUNCTION ======
# =====================================================
