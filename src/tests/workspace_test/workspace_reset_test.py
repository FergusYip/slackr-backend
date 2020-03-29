'''System tests for workspace_reset'''
import pytest
from auth import auth_logout
from channels import channels_listall
from other import users_all
from workspace import workspace_reset
from error import AccessError


def test_workspace_reset_user(reset, new_user):  # pylint: disable=W0613
    '''Test that the number of users are reset'''
    user_a = new_user(email='user_a@email.com')
    new_user(email='user_b@email.com')
    all_users = users_all(user_a['token'])
    assert len(all_users['users']) == 2

    workspace_reset()

    user_c = new_user(email='user_c@email.com')
    all_users = users_all(user_c['token'])

    assert len(all_users['users']) == 1


def test_workspace_reset_channels(reset, new_user, new_channel):  # pylint: disable=W0613
    '''Test that the number of users are reset'''
    user = new_user()
    new_channel(user, 'Channel A')
    new_channel(user, 'Channel B')

    all_channels = channels_listall(user['token'])

    assert len(all_channels['channels']) == 2

    workspace_reset()

    user = new_user()
    all_channels = channels_listall(user['token'])
    assert len(all_channels['channels']) == 0


def test_workspace_reset_old_token(reset, new_user):  # pylint: disable=W0613
    '''Test that the old tokens are invalid is reset'''
    user = new_user()
    workspace_reset()
    with pytest.raises(AccessError):
        auth_logout(user['token'])
