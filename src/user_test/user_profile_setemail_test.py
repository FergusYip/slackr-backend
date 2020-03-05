import user
import auth
import pytest
from error import AccessError, InputError

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
