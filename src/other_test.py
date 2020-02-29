import auth
import other
import user
import pytest


def test_users_all_basic():
    avery = auth.register('averylogrono@email.com',
                          'averylogrono', 'Avery', 'Logrono')
    user.profile_sethandle(avery['token'], 'averylogrono')

    avery_profile = user.profile(avery['token'], avery['u_id'])['user']
    all_users = other.users_all(avery['token'])

    assert avery_profile in all_users['users']
