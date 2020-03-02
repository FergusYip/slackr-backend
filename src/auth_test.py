import auth
import pytest
from error import InputError


valid_emails = ['latonyaDAVISON@email.com',
                '123456789@email.com',
                'lantonyDAVISON123@email.com',
                '!#$%&*+- /=?^_`{ | }~@email.com']

invalid_email_at_sign = ['latonyadavison.com',
                         'latonya@davison@email.com']

invalid_email_dot_sign = ['.latonyadavison@email.com',
                          'latonyadavison.@email.com',
                          'latonya..davison.@email.com']

invalid_email_length = ['i' * 65 + '@email.com',
                        'i' * 64 + '@' + 'd' * 192 + '.com']


def test_register_return_type():
    user = auth.register('theresavanaria@email.com', 'password',
                         'Theresa', 'Vanaria')
    assert isinstance(user['u_id'], int) == True
    assert isinstance(user['token'], str) == True


def test_register_email():
    # Valid email
    for email in valid_emails:
        assert auth.register(email, 'password', 'First', 'Last')

    # Invalid email with @ sign problems
    for email in invalid_email_at_sign:
        with pytest.raises(InputError) as e:
            assert auth.register(email, 'password', 'First', 'Last')

    # Invalid email with . sign problems
    for email in invalid_email_dot_sign:
        with pytest.raises(InputError) as e:
            assert auth.register(email, 'password', 'First', 'Last')

    # Invalid email with length problems
    for email in invalid_email_length:
        with pytest.raises(InputError) as e:
            assert auth.register(email, 'password', 'First', 'Last')


def test_register_duplicate():
    # Setup 'existing' user
    auth.register('durumarion@email.com', 'password', 'Duru', 'Marion')

    with pytest.raises(InputError) as e:
        assert auth.register('durumarion@email.com',
                             'password', 'Duru', 'Marion')


def test_register_password():
    # Valid
    assert auth.register('richardoutterridge@email.com',
                         '123456', 'Richard', 'Outterridge')

    # <6 Password Length
    with pytest.raises(InputError) as e:
        assert auth.register('richardoutterridge@email.com',
                             '12345', 'Richard', 'Outterridge')


def test_register_first_name():
    # Valid
    assert auth.register('valid@email.com', 'password', 'Giltbert', 'Blue')

    # <1 Character
    with pytest.raises(InputError) as e:
        assert auth.register('valid@email.com', 'password', '', 'Blue')

    # >50 Characters
    with pytest.raises(InputError) as e:
        assert auth.register('valid@email.com', 'password', 'a' * 50, 'Blue')


def test_register_last_name():
    # Valid
    assert auth.register('valid@email.com', 'password', 'Aziza', 'Addens')

    # <1 Character
    with pytest.raises(InputError) as e:
        assert auth.register('valid@email.com', 'password', 'Aziza', '')

    # >50 Characters
    with pytest.raises(InputError) as e:
        assert auth.register('valid@email.com', 'password', 'Aziza', 'a' * 50)


@pytest.fixture
def paris():
    return auth.register('pariscler@email.com', 'pariscler0229', 'Paris', 'Cler')


def test_logout(paris):
    assert auth.logout(paris['token'])['is_success'] == True


def test_logout_invalid_token(paris):
    assert auth.logout(paris['token'])['is_success'] == True

    # input invalidated token into function
    assert auth.logout(paris['token'])['is_success'] == True


def test_login(paris):
    paris_login = auth.login('pariscler@email.com', 'pariscler0229')
    assert paris_login['u_id'] == paris['u_id']

    # Password is not correct
    with pytest.raises(InputError) as e:
        assert auth.login('pariscler@email.com', 'incorrect_password')

    # Email entered does not belong to a user
    with pytest.raises(InputError) as e:
        assert auth.login('non_existent_user@email.com', '12345678')


def test_login_multiple_sessions(paris):
    session_1 = auth.login('pariscler@email.com', 'pariscler0229')
    session_2 = auth.login('pariscler@email.com', 'pariscler0229')
    session_3 = auth.login('pariscler@email.com', 'pariscler0229')

    session_tokens = [paris['token'],
                      session_1['token'],
                      session_2['token'],
                      session_3['token']]

    # Verify that all session_tokens are unique
    assert len(set(session_tokens)) == len(session_tokens)

# Don't know how to test auth_login with invalid email since an invalid email
# will never belong to a register user. This means that if auth_login is given
# an invalid email, it would return two InputErrors

# def test_login_email():
#     # Valid email
#     for email in valid_emails:
#         assert auth.login(email, 'password')

#     # Invalid email with @ sign problems
#     for email in invalid_email_at_sign:
#         with pytest.raises(InputError) as e:
#             assert auth.login(email, 'password')

#     # Invalid email with . sign problems
#     for email in invalid_email_dot_sign:
#         with pytest.raises(InputError) as e:
#             assert auth.login(email, 'password')

#     # Invalid email with length problems
#     for email in invalid_email_length:
#         with pytest.raises(InputError) as e:
#             assert auth.login(email, 'password')
