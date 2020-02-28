import auth
import pytest
from error import InputError


def test_register_return_type():
    user = auth.register('theresavanaria@email.com', 'password',
                         'Theresa', 'Vanaria')
    isinstance(user['u_id'], int) == True
    isinstance(user['token'], str) == True


def test_register_email():
    # Valid uppwercase and lowercase english characters
    auth.register('latonyaDAVISON@email.com', 'password', 'Latonya', 'Davison')

    # No @
    with pytest.raises(InputError) as e:
        auth.register('latonyadavison.com', 'password', 'Latonya', 'Davison')

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
    pass
