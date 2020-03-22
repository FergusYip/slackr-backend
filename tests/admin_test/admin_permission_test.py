import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_admin_invalid_u_id(reset, new_user):
    '''Test user_all with invalid token'''

    admin = new_user(email='admin@slackr.com')

    permission_input = {
        'token': admin['token'],
        'u_id': -1,
        'permission_id': 1
    }

    error = requests.post(f'{BASE_URL}/admin/userpermission/change',
                          json=permission_input)

    with pytest.raises(requests.HTTPError):
        requests.Response.raise_for_status(error)


def test_admin_invalid_permission(reset, new_user):
    '''Test user_all with invalid token'''

    admin = new_user(email='admin@slackr.com')
    member = new_user(email='pleb@slackr.com')

    permission_input = {
        'token': admin['token'],
        'u_id': member['u_id'],
        'permission_id': -1
    }

    error = requests.post(f'{BASE_URL}/admin/userpermission/change',
                          json=permission_input)

    with pytest.raises(requests.HTTPError):
        requests.Response.raise_for_status(error)


def test_admin_not_owner(reset, new_user):
    '''Test user_all with invalid token'''

    admin = new_user(email='admin@slackr.com')
    member = new_user(email='pleb@slackr.com')

    permission_input = {
        'token': member['token'],
        'u_id': admin['u_id'],
        'permission_id': 1
    }

    error = requests.post(f'{BASE_URL}/admin/userpermission/change',
                          json=permission_input)

    with pytest.raises(requests.HTTPError):
        requests.Response.raise_for_status(error)


def test_admin_invalid_token(reset, new_user, invalid_token):
    '''Test user_all with invalid token'''

    member = new_user(email='pleb@slackr.com')

    permission_input = {
        'token': invalid_token,
        'u_id': member['u_id'],
        'permission_id': 1
    }

    error = requests.post(f'{BASE_URL}/admin/userpermission/change',
                          json=permission_input)

    # with pytest.raises(requests.HTTPError):
    requests.Response.raise_for_status(error)


# def test_admin_base(reset, new_user):
#     '''Test user_all with invalid token'''

#     admin = new_user(email='admin@slackr.com')
#     member = new_user(email='pleb@slackr.com')

#     permission_input = {
#         'token': admin['token'],
#         'u_id': member['u_id'],
#         'permission_id': 1
#     }

#     requests.post(f'{BASE_URL}/admin/userpermission/change',
#                   json=permission_input)
