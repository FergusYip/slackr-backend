import user
import auth
import pytest
from error import AccessError, InputError

# =====================================================
# ====== TESTING USER PROFILE SETNAME FUNCTION ========
# =====================================================

def test_averagecase_setname():
    # Creating a user and calling user_profile_setname without raising an error.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Lorem', 'Ipsum')
    user.user_profile_setname(new_user['token'], 'Ipsum', 'Lorem')
    profile_info = user.user_profile(new_user['token'], new_user['u_id'])
    assert profile_info['name_first'] == 'Ipsum'
    assert profile_info['name_last'] == 'Lorem'

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
