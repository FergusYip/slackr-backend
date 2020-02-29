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
    isinstance(user['u_id'], int) == True
    isinstance(user['token'], str) == True


def test_register_email():
    # Valid email
    for email in valid_emails:
        auth.register(email, 'password', 'First', 'Last')

    # Invalid email with @ sign problems
    for email in invalid_email_at_sign:
        with pytest.raises(InputError) as e:
            auth.register(email, 'password', 'First', 'Last')

    # Invalid email with . sign problems
    for email in invalid_email_dot_sign:
        with pytest.raises(InputError) as e:
            auth.register(email, 'password', 'First', 'Last')

    # Invalid email with length problems
    for email in invalid_email_length:
        with pytest.raises(InputError) as e:
            auth.register(email, 'password', 'First', 'Last')


def test_register_duplicate():
    # Setup 'existing' user
    auth.register('durumarion@email.com', 'password', 'Duru', 'Marion')

    with pytest.raises(InputError) as e:
        auth.register('durumarion@email.com', 'password', 'Duru', 'Marion')


def test_register_password():
    # Valid
    auth.register('richardoutterridge@email.com',
                  '123456', 'Richard', 'Outterridge')

    # <6 Password Length
    with pytest.raises(InputError) as e:
        auth.register('richardoutterridge@email.com',
                      '12345', 'Richard', 'Outterridge')


def test_register_first_name():
    # Valid
    auth.register('valid@email.com', 'password', 'Giltbert', 'Blue')

    # <1 Character
    with pytest.raises(InputError) as e:
        auth.register('valid@email.com', 'password', '', 'Blue')

    # >50 Characters
    with pytest.raises(InputError) as e:
        auth.register('valid@email.com', 'password', 'a' * 50, 'Blue')


def test_register_last_name():
    # Valid
    auth.register('valid@email.com', 'password', 'Aziza', 'Addens')

    # <1 Character
    with pytest.raises(InputError) as e:
        auth.register('valid@email.com', 'password', 'Aziza', '')

    # >50 Characters
    with pytest.raises(InputError) as e:
        auth.register('valid@email.com', 'password', 'Aziza', 'a' * 50)


def test_logout():
    paris = auth.register('pariscler@email.com',
                          'pariscler0229', 'Paris', 'Cler')
    assert auth.logout(paris['token'])['is_success'] == True


def test_login():
    paris = auth.register('pariscler@email.com',
                          'pariscler0229', 'Paris', 'Cler')
    assert auth.logout(paris['token'])['is_success'] == True

    paris_login = auth.login('pariscler@email.com', 'pariscler0229')
    assert paris_login['u_id'] == paris['u_id']

    # Password is not correct
    with pytest.raises(InputError) as e:
        auth.login('pariscler@email.com', 'incorrect_password')

    # Email entered does not belong to a user
    with pytest.raises(InputError) as e:
        auth.login('non_existent_user@email.com', '12345678')


# Don't know how to test auth_login with invalid email since an invalid email
# will never belong to a register user. This means that if auth_login is given
# an invalid email, it would return two InputErrors

# def test_login_email():
#     # Valid email
#     for email in valid_emails:
#         auth.login(email, 'password')

#     # Invalid email with @ sign problems
#     for email in invalid_email_at_sign:
#         with pytest.raises(InputError) as e:
#             auth.login(email, 'password')

#     # Invalid email with . sign problems
#     for email in invalid_email_dot_sign:
#         with pytest.raises(InputError) as e:
#             auth.login(email, 'password')

#     # Invalid email with length problems
#     for email in invalid_email_length:
#         with pytest.raises(InputError) as e:
#             auth.login(email, 'password')
