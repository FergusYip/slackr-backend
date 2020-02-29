import auth
import other
import user
import pytest


def test_users_all_basic():
    avery = auth.register('averylogrono@email.com',
                          'averylogrono', 'Avery', 'Logrono')
    user.profile_sethandle(avery['token'], 'averylogrono')

    all_users = other.users_all(avery['token'])
    assert all_users['users'][0]['u_id'] == avery['u_id']
    assert all_users['users'][0]['email'] == 'user.name@email.com'
    assert all_users['users'][0]['name_first'] == 'First'
    assert all_users['users'][0]['name_last'] == 'Last'
    assert all_users['users'][0]['handle_str'] == 'averylogrono'
