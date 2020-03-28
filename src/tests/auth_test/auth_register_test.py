''' System tests for auth_register'''
import pytest
import auth
import user
from error import InputError


def test_register_return_type(reset):  # pylint: disable=W0613
    '''Test the types of values returned by auth_register'''

    register = auth.auth_register('theresavanaria@email.com', 'password',
                                  'Theresa', 'Vanaria')
    assert isinstance(register['u_id'], int)
    assert isinstance(register['token'], str)


def test_register_duplicate(reset):  # pylint: disable=W0613
    '''Test the registration of multiple users with the same email'''

    # Setup 'existing' user
    auth.auth_register('durumarion@email.com', 'password', 'Duru', 'Marion')

    with pytest.raises(InputError):
        auth.auth_register('durumarion@email.com', 'password', 'Duru',
                           'Marion')


def test_register_password(reset):  # pylint: disable=W0613
    '''Test the input of a valid password length into auth_register'''

    auth.auth_register('richardoutterridge@email.com', '123456', 'Richard',
                       'Outterridge')


def test_register_short_password(reset):  # pylint: disable=W0613
    '''Test the input of an invalid password length into auth_register'''

    # <6 Password Length
    with pytest.raises(InputError):
        auth.auth_register('richardoutterridge@email.com', '12345', 'Richard',
                           'Outterridge')


def test_register_long_password(reset):  # pylint: disable=W0613
    '''Test the input of a password with 32 characters into auth_register'''

    # 32 character password that is within the (assumed) maximum length for password
    auth.auth_register('richardoutterridge@email.com', 'i' * 32, 'Richard',
                       'Outterridge')


def test_register_first_name(reset):  # pylint: disable=W0613
    '''Test the input of various first name lengths into auth_register'''

    auth.auth_register('valid@email.com', 'password', 'Giltbert', 'Blue')


def test_register_short_first_name(reset):  # pylint: disable=W0613
    '''Test the input of first name that is too short into auth_register'''

    # <1 Character
    with pytest.raises(InputError):
        auth.auth_register('valid@email.com', 'password', '', 'Blue')


def test_register_long_first_name(reset):  # pylint: disable=W0613
    '''Test the input of first name that is too long into auth_register'''

    # >50 Characters
    with pytest.raises(InputError):
        auth.auth_register('valid@email.com', 'password', 'a' * 51, 'Blue')


def test_register_last_name(reset):  # pylint: disable=W0613
    '''Test the input of a valid last name length into auth_register'''

    auth.auth_register('valid@email.com', 'password', 'Aziza', 'Addens')


def test_register_short_last_name(reset):  # pylint: disable=W0613
    '''Test the input of last name that is too short into auth_register'''

    # <1 Character
    with pytest.raises(InputError):
        auth.auth_register('valid@email.com', 'password', 'Aziza', '')


def test_register_long_last_name(reset):  # pylint: disable=W0613
    '''Test the input of last name that is too long into auth_register'''

    # >50 Characters
    with pytest.raises(InputError):
        auth.auth_register('valid@email.com', 'password', 'Aziza', 'a' * 51)


def test_register_handle(reset):  # pylint: disable=W0613
    '''Test that the handle generated by auth_register matches assumption'''

    test_user = auth.auth_register('valid@email.com', 'password', 'First',
                                   'Last')
    test_profile = user.user_profile(test_user['token'], test_user['u_id'])
    assert test_profile['handle_str'] == 'firstlast'


def test_register_unique_handle(reset):  # pylint: disable=W0613
    '''Test that handles generated by auth_register are unique'''

    user_1 = auth.auth_register('valid@email.com', 'password', 'First', 'Last')
    user_profile_1 = user.user_profile(user_1['token'], user_1['u_id'])

    user_2 = auth.auth_register('avalid@email.com', 'password', 'First',
                                'Last')
    user_profile_2 = user.user_profile(user_2['token'], user_2['u_id'])

    assert user_profile_1['handle_str'] != user_profile_2['handle_str']


def test_register_long_handle(reset):  # pylint: disable=W0613
    '''Test that handles generated by auth_register are cut off at 20 characters'''

    test_user = auth.auth_register('valid@email.com', 'password',
                                   '123456789testing', '123456789testing')
    test_profile = user.user_profile(test_user['token'], test_user['u_id'])
    assert test_profile['handle_str'] == '123456789testing1234'


def test_register_unique_token(reset):  # pylint: disable=W0613
    '''Test that the tokens provided to each user is unique'''
    user_1 = auth.auth_register('user_1@email.com', 'password',
                                '123456789testing', '123456789testing')
    user_2 = auth.auth_register('user_2@email.com', 'password',
                                '123456789testing', '123456789testing')

    assert user_1['token'] != user_2['token']


def test_register_email_valid(reset, valid_emails):  # pylint: disable=W0613
    '''Test input of valid emails into auth_register'''

    for email in valid_emails:
        auth.auth_register(email, 'password', 'First', 'Last')


def test_register_email_invalid(reset, invalid_emails):  # pylint: disable=W0613
    '''Test input of invalid emails into auth_register'''

    for email in invalid_emails:
        with pytest.raises(InputError):
            auth.auth_register(email, 'password', 'First', 'Last')
