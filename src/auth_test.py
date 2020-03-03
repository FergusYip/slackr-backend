import pytest
import auth
import user
from error import InputError

valid_emails = ('latonyaDAVISON@email.com', '123456789@email.com',
                'lantonyDAVISON123@email.com',
                '!#$%&*+- /=?^_`{ | }~@email.com')

invalid_email_at_sign = ('latonyadavison.com', 'latonya@davison@email.com')

invalid_email_dot_sign = ('.latonyadavison@email.com',
                          'latonyadavison.@email.com',
                          'latonya..davison.@email.com')

invalid_email_length = ('i' * 65 + '@email.com',
                        'i' * 64 + '@' + 'd' * 192 + '.com')


def test_register_return_type():
    user = auth.auth_register('theresavanaria@email.com', 'password',
                              'Theresa', 'Vanaria')
    assert isinstance(user['u_id'], int)
    assert isinstance(user['token'], str)


def test_register_email():
    # Valid email
    for email in valid_emails:
        assert auth.auth_register(email, 'password', 'First', 'Last')

    # Invalid email with @ sign problems
    for email in invalid_email_at_sign:
        with pytest.raises(InputError) as e:
            assert auth.auth_register(email, 'password', 'First', 'Last')

    # Invalid email with . sign problems
    for email in invalid_email_dot_sign:
        with pytest.raises(InputError) as e:
            assert auth.auth_register(email, 'password', 'First', 'Last')

    # Invalid email with length problems
    for email in invalid_email_length:
        with pytest.raises(InputError) as e:
            assert auth.auth_register(email, 'password', 'First', 'Last')


def test_register_duplicate():
    # Setup 'existing' user
    auth.auth_register('durumarion@email.com', 'password', 'Duru', 'Marion')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('durumarion@email.com', 'password', 'Duru',
                                  'Marion')


def test_register_password():
    # Valid
    assert auth.auth_register('richardoutterridge@email.com', '123456',
                              'Richard', 'Outterridge')

    # <6 Password Length
    with pytest.raises(InputError) as e:
        assert auth.auth_register('richardoutterridge@email.com', '12345',
                                  'Richard', 'Outterridge')

    # 32 character password
    assert auth.auth_register('richardoutterridge@email.com', 'i' * 32,
                              'Richard', 'Outterridge')


def test_register_first_name():
    # Valid
    assert auth.auth_register('valid@email.com', 'password', 'Giltbert',
                              'Blue')

    # <1 Character
    with pytest.raises(InputError) as e:
        assert auth.auth_register('valid@email.com', 'password', '', 'Blue')

    # >50 Characters
    with pytest.raises(InputError) as e:
        assert auth.auth_register('valid@email.com', 'password', 'a' * 50,
                                  'Blue')


def test_register_last_name():
    # Valid
    assert auth.auth_register('valid@email.com', 'password', 'Aziza', 'Addens')

    # <1 Character
    with pytest.raises(InputError) as e:
        assert auth.auth_register('valid@email.com', 'password', 'Aziza', '')

    # >50 Characters
    with pytest.raises(InputError) as e:
        assert auth.auth_register('valid@email.com', 'password', 'Aziza',
                                  'a' * 50)


def test_register_handle():
    test_user = auth.auth_register('valid@email.com', 'password', 'First',
                                   'Last')
    test_profile = user.user_profile(test_user['token'], test_user['u_id'])
    assert test_profile['user']['handle_str'] == 'firstlast'


def test_register_unique_handle():
    user_1 = auth.auth_register('valid@email.com', 'password', 'First', 'Last')
    user_profile_1 = user.user_profile(user_1['token'], user_1['u_id'])

    user_2 = auth.auth_register('avalid@email.com', 'password', 'First',
                                'Last')
    user_profile_2 = user.user_profile(user_2['token'], user_2['u_id'])

    assert user_profile_1['user']['handle_str'] != user_profile_2['user'][
        'handle_str']


def test_register_long_handle():
    test_user = auth.auth_register('valid@email.com', 'password',
                                   '123456789testing', '123456789testing')
    test_profile = user.user_profile(test_user['token'], test_user['u_id'])
    assert test_profile['user']['handle_str'] == '123456789testing1234'


@pytest.fixture
def paris():
    return auth.auth_register('pariscler@email.com', 'pariscler0229', 'Paris',
                              'Cler')


def test_logout(paris):
    assert auth.auth_logout(paris['token'])['is_success']


def test_logout_invalid_token(paris):
    assert auth.auth_logout(paris['token'])['is_success']

    # input invalidated token into function
    assert auth.auth_logout(paris['token'])['is_success']


def test_login(paris):
    paris_login = auth.auth_login('pariscler@email.com', 'pariscler0229')
    assert paris_login['u_id'] == paris['u_id']

    # Password is not correct
    with pytest.raises(InputError) as e:
        assert auth.auth_login('pariscler@email.com', 'incorrect_password')

    # Email entered does not belong to a user
    with pytest.raises(InputError) as e:
        assert auth.auth_login('non_existent_user@email.com', '12345678')


def test_login_multiple_sessions(paris):
    session_1 = auth.auth_login('pariscler@email.com', 'pariscler0229')
    session_2 = auth.auth_login('pariscler@email.com', 'pariscler0229')
    session_3 = auth.auth_login('pariscler@email.com', 'pariscler0229')

    session_tokens = [
        paris['token'], session_1['token'], session_2['token'],
        session_3['token']
    ]

    # Verify that all session_tokens are unique
    assert len(set(session_tokens)) == len(session_tokens)


# Don't know how to test auth_login with invalid email since an invalid email
# will never belong to a register user. This means that if auth_login is given
# an invalid email, it would return two InputErrors

# def test_login_email():
#     # Valid email
#     for email in valid_emails:
#         assert auth.auth_login(email, 'password')

#     # Invalid email with @ sign problems
#     for email in invalid_email_at_sign:
#         with pytest.raises(InputError) as e:
#             assert auth.auth_login(email, 'password')

#     # Invalid email with . sign problems
#     for email in invalid_email_dot_sign:
#         with pytest.raises(InputError) as e:
#             assert auth.auth_login(email, 'password')

#     # Invalid email with length problems
#     for email in invalid_email_length:
#         with pytest.raises(InputError) as e:
#             assert auth.auth_login(email, 'password')
