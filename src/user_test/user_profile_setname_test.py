import user
import auth
import pytest
from error import AccessError, InputError

# =====================================================
# ====== TESTING USER PROFILE SETNAME FUNCTION ========
# =====================================================

def test_averagecase_setname(test_user):

    ''' Testing an average case where a user will change their name to a valid
    choice. '''

    user.user_profile_setname(test_user['token'], 'Ipsum', 'Lorem')
    profile_info = user.user_profile(test_user['token'], test_user['u_id'])

    assert profile_info['user']['name_first'] == 'Ipsum'
    assert profile_info['user']['name_last'] == 'Lorem'


def test_firstzerocharacter(test_user):

    ''' Testing that the user_profile_setname function will raise an InputError
    if the value of the first name contains zero characters. '''

    with pytest.raises(InputError):
        user.user_profile_setname(test_user['token'], '', 'Lorem')


def test_firstoverfifty(test_user):

    ''' Testing that the user_profile_setname function will raise an InputError
    if the value of the first name is greater than 50 characters (50 uninclusive). '''

    with pytest.raises(InputError):
        user.user_profile_setname(test_user['token'], 'i' * 51, 'Lorem')


def test_lastzerocharacter(test_user):

    ''' Testing that the user_profile_setname function will raise an InputError
    if the value of the last name contains zero characters. '''

    with pytest.raises(InputError):
        user.user_profile_setname(test_user['token'], 'Ipsum', '')


def test_lastoverfifty(test_user):

    ''' Testing that the user_profile_setname function will raise an InputError
    if the value of the last name is greater than 50 characters (50 uninclusive). '''

    with pytest.raises(InputError):
        user.user_profile_setname(test_user['token'], 'Ipsum', 'i' * 51)


def invalidtoken_namechange():

    ''' Testing that an AccessError is raised if the token passed to the
    user_profile_setname function is invalid. '''

    with pytest.raises(AccessError):
        user.user_profile_setname('NOTAVALIDTOKEN', 'Johnny', 'McJohnny')
