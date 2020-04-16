''' System tests for admin_permission_change'''
import pytest
import admin
from error import InputError, AccessError


def test_admin_invalid_u_id(reset, new_user):
    '''Test function with invalid u_id value'''

    admin_user = new_user(email='admin@slackr.com')

    with pytest.raises(InputError):
        admin.admin_userpermission_change(admin_user['token'], -1, 1)


def test_admin_invalid_permission(reset, new_user):
    '''Test function with invalid permission value'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    with pytest.raises(InputError):
        admin.admin_userpermission_change(admin_user['token'],
                                          member_user['u_id'], -1)


def test_admin_not_owner(reset, new_user):
    '''Test if function raises InputError if the requesting user is not admin'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    with pytest.raises(AccessError):
        admin.admin_userpermission_change(member_user['token'],
                                          admin_user['u_id'], 1)


def test_admin_invalid_token(reset, new_user, invalid_token):
    '''Test admin_userpermission_change with invalid token'''

    member = new_user(email='pleb@slackr.com')

    with pytest.raises(AccessError):
        admin.admin_userpermission_change(invalid_token, member['u_id'], 1)


def test_admin_userpermission_change(reset, new_user):
    '''Test that newly assigned admin user can modify other users'''

    admin_user = new_user(email='admin@slackr.com')
    member_a = new_user(email='plebian@slackr.com')
    member_b = new_user(email='pleb@slackr.com')

    admin.admin_userpermission_change(admin_user['token'], member_a['u_id'], 1)

    admin.admin_userpermission_change(member_a['token'], member_b['u_id'], 1)


def test_admin_userpermission_change_self(reset, new_user):
    '''Test that error is raised when change would result in no owener'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    admin.admin_userpermission_change(admin_user['token'], member_user['u_id'],
                                      1)
    admin.admin_userpermission_change(admin_user['token'], admin_user['u_id'],
                                      2)

    with pytest.raises(AccessError):
        admin.admin_userpermission_change(admin_user['token'],
                                          admin_user['u_id'], 1)


def test_admin_userpermission_change_no_owner(reset, new_user):
    '''Test that error is raised when change would result in no owener'''

    admin_user = new_user(email='admin@slackr.com')

    with pytest.raises(InputError):
        admin.admin_userpermission_change(admin_user['token'],
                                          admin_user['u_id'], 2)
