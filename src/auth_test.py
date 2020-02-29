import auth
import pytest
from error import InputError


def test_register_return_type():
    user = auth.register('theresavanaria@email.com', 'password',
                         'Theresa', 'Vanaria')
    isinstance(user['u_id'], int) == True
    isinstance(user['token'], str) == True


def test_register_email_valid():
    # Valid uppwercase and lowercase english characters
    auth.register('latonyaDAVISON@email.com', 'password', 'Latonya', 'Davison')

    # Valid digits
    auth.register('123456789@email.com', 'password', 'Latonya', 'Davison')

    # Valid mix of digits and english characters
    auth.register('lantonyDAVISON123@email.com',
                  'password', 'Latonya', 'Davison')

    # Valid printable characters
    auth.register('!#$%&*+- /=?^_`{ | }~@email.com',
                  'password', 'Latonya', 'Davison')


def test_register_email_at_sign():
    # No @
    with pytest.raises(InputError) as e:
        auth.register('latonyadavison.com', 'password', 'Latonya', 'Davison')

    # Two @
    with pytest.raises(InputError) as e:
        auth.register('latonya@davison@email.com',
                      'password', 'Latonya', 'Davison')


def test_register_email_dot_sign():
    # Local-part starting with .
    with pytest.raises(InputError) as e:
        auth.register('.latonyadavison@email.com',
                      'password', 'Latonya', 'Davison')

    # Local-part ending with .
    with pytest.raises(InputError) as e:
        auth.register('latonyadavison.@email.com',
                      'password', 'Latonya', 'Davison')

    # Local-part with consecutive .
    with pytest.raises(InputError) as e:
        auth.register('latonya..davison.@email.com',
                      'password', 'Latonya', 'Davison')


def test_register_email_length():
    # Local-part longer than 64 characters
    with pytest.raises(InputError) as e:
        auth.register('i' * 65 + '@email.com',
                      'password', 'Latonya', 'Davison')

    # Email length longer than 256 characters
    with pytest.raises(InputError) as e:
        auth.register('i' * 64 + '@' + 'd' * 192 + '.com',
                      'password', 'Latonya', 'Davison')


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


def test_login():
    pass


def test_logout():
    paris = auth.register('pariscler@email.com',
                          'pariscler0229', 'Paris', 'Cler')
    assert auth.logout(paris['token']) == True
