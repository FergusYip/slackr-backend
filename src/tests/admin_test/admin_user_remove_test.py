''' System tests for admin_user_remove'''
import pytest
import admin
import other
import channel
import channels
import message as msg
from error import InputError, AccessError


def test_admin_user_remove_insufficient_params(reset, new_user):
    '''Test function with insufficient parameters'''

    with pytest.raises(InputError):
        admin.admin_user_remove(None, None)


def test_admin_user_remove_invalid_u_id(reset, new_user):
    '''Test function with invalid u_id value'''

    admin_user = new_user(email='admin@slackr.com')

    with pytest.raises(InputError):
        admin.admin_user_remove(admin_user['token'], -1)


def test_admin_user_remove_not_owner(reset, new_user):
    '''Test if function raises InputError if the requesting user is not admin'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    with pytest.raises(AccessError):
        admin.admin_user_remove(member_user['token'], admin_user['u_id'])


def test_admin_user_remove_invalid_token(reset, new_user, invalid_token):
    '''Test function with invalid token'''

    member_user = new_user(email='pleb@slackr.com')

    with pytest.raises(AccessError):
        admin.admin_user_remove(invalid_token, member_user['u_id'])


def test_admin_user_remove_delete_self(reset, new_user):
    '''Test that the only admin cannot remove themself'''

    admin_user = new_user(email='admin@slackr.com')

    with pytest.raises(InputError):
        admin.admin_user_remove(admin_user['token'], admin_user['u_id'])


def test_admin_user_remove_valid_removal(reset, new_user):
    '''Test that function removes the user'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    admin.admin_user_remove(admin_user['token'], member_user['u_id'])

    all_users = other.users_all(admin_user['token'])['users']

    assert len(all_users) == 1


def test_admin_user_remove_after_removal_registration(reset, new_user):
    '''Test that the results of removing a user in regards to registration'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    admin.admin_user_remove(admin_user['token'], member_user['u_id'])

    # Test that other users can use the same email
    member_user_2 = new_user(email='pleb@slackr.com')

    assert member_user['u_id'] != member_user_2['u_id']


def test_admin_user_remove_after_removal_channel(reset, new_user, new_channel):
    '''Test that the results of removing a user in regards to channels'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    test_channel = channels.channels_create(admin_user['token'], 'Channel',
                                            True)
    channel.channel_join(member_user['token'], test_channel['channel_id'])

    channel_members = channel.channel_details(
        admin_user['token'], test_channel['channel_id'])['all_members']
    assert len(channel_members) == 2

    admin.admin_user_remove(admin_user['token'], member_user['u_id'])

    channel_members = channel.channel_details(
        admin_user['token'], test_channel['channel_id'])['all_members']
    assert len(channel_members) == 1


def test_admin_user_remove_after_removal_msgs(reset, new_user, new_channel):
    '''Test that the results of removing a user in regards to messages'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    test_channel = channels.channels_create(admin_user['token'], 'Channel',
                                            True)
    channel.channel_join(member_user['token'], test_channel['channel_id'])

    channel_members = channel.channel_details(
        admin_user['token'], test_channel['channel_id'])['all_members']
    assert len(channel_members) == 2

    msg.message_send(member_user['token'], test_channel['channel_id'], 'Hello')

    channel_msgs = channel.channel_messages(admin_user['token'],
                                            test_channel['channel_id'],
                                            0)['messages']
    assert len(channel_msgs) == 1

    admin.admin_user_remove(admin_user['token'], member_user['u_id'])

    # Check that message remains in the channel
    channel_msgs = channel.channel_messages(admin_user['token'],
                                            test_channel['channel_id'],
                                            0)['messages']
    assert len(channel_msgs) == 1


def test_admin_user_remove_after_removal_reacts(reset, new_user, new_channel):
    '''Test that the results of removing a user in regards to reacts'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    test_channel = channels.channels_create(admin_user['token'], 'Channel',
                                            True)
    channel.channel_join(member_user['token'], test_channel['channel_id'])

    channel_members = channel.channel_details(
        admin_user['token'], test_channel['channel_id'])['all_members']
    assert len(channel_members) == 2

    test_msg = msg.message_send(member_user['token'],
                                test_channel['channel_id'], 'Hello')
    msg.message_react(member_user['token'], test_msg['message_id'], 1)

    channel_msgs = channel.channel_messages(admin_user['token'],
                                            test_channel['channel_id'],
                                            0)['messages']
    assert len(channel_msgs) == 1
    assert len(channel_msgs[0]['reacts']) == 1

    admin.admin_user_remove(admin_user['token'], member_user['u_id'])

    # Check that react remains in the channel
    channel_msgs = channel.channel_messages(admin_user['token'],
                                            test_channel['channel_id'],
                                            0)['messages']
    assert len(channel_msgs) == 1
    assert len(channel_msgs[0]['reacts']) == 1


def test_admin_user_remove_after_removal_token(reset, new_user, new_channel):
    '''Test that the results of removing a user in regards to the user token'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    channels.channels_create(member_user['token'], 'Channel', True)

    admin.admin_user_remove(admin_user['token'], member_user['u_id'])

    with pytest.raises(AccessError):
        channels.channels_create(member_user['token'], 'Channel', True)
