import pytest
import auth
import other
import user
from error import AccessError


def test_users_all_basic():
    avery = auth.auth_register('averylogrono@email.com', 'averylogrono',
                               'Avery', 'Logrono')

    avery_profile = user.user_profile(avery['token'], avery['u_id'])['user']
    all_users = other.users_all(avery['token'])

    assert avery_profile in all_users['users']


def test_users_all_invalid_token(invalid_token):
    with pytest.raises(AccessError):
        other.users_all(invalid_token)
