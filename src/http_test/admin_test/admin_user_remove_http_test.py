'''Pytest script for testing /admin/user/remove route'''
import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_user_remove_insufficient_params(reset):
    '''Test function with insufficient parameters'''

    with pytest.raises(requests.HTTPError):
        requests.delete(f'{BASE_URL}/admin/user/remove',
                        json={}).raise_for_status()


def test_user_remove_invalid_u_id(reset, new_user):
    '''Test function with invalid u_id value'''

    admin_user = new_user(email='admin@slackr.com')

    remove_input = {'token': admin_user['token'], 'u_id': -1}

    with pytest.raises(requests.HTTPError):
        requests.delete(f'{BASE_URL}/admin/user/remove',
                        json=remove_input).raise_for_status()


def test_user_remove_not_owner(reset, new_user):
    '''Test if function raises InputError if the requesting user is not admin'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    remove_input = {'token': member_user['token'], 'u_id': admin_user['u_id']}

    with pytest.raises(requests.HTTPError):
        requests.delete(f'{BASE_URL}/admin/user/remove',
                        json=remove_input).raise_for_status()


def test_user_remove_invalid_token(reset, new_user, invalid_token):
    '''Test function with invalid token'''

    member_user = new_user(email='pleb@slackr.com')

    remove_input = {'token': invalid_token, 'u_id': member_user['u_id']}

    with pytest.raises(requests.HTTPError):
        requests.delete(f'{BASE_URL}/admin/user/remove',
                        json=remove_input).raise_for_status()


def test_user_remove_delete_self(reset, new_user):
    '''Test that the only admin cannot remove themself'''

    admin_user = new_user(email='admin@slackr.com')

    remove_input = {'token': admin_user['token'], 'u_id': admin_user['u_id']}

    with pytest.raises(requests.HTTPError):
        requests.delete(f'{BASE_URL}/admin/user/remove',
                        json=remove_input).raise_for_status()


def test_user_remove_valid_removal(reset, new_user):
    '''Test that function removes the user'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    remove_input = {'token': admin_user['token'], 'u_id': member_user['u_id']}

    requests.delete(f'{BASE_URL}/admin/user/remove',
                    json=remove_input).raise_for_status()

    all_users = requests.get(f'{BASE_URL}/users/all',
                             params={
                                 'token': admin_user['token']
                             }).json()['users']

    assert len(all_users) == 1


def test_user_remove_after_removal_registration(reset, new_user):
    '''Test that the results of removing a user in regards to registration'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    remove_input = {'token': admin_user['token'], 'u_id': member_user['u_id']}

    requests.delete(f'{BASE_URL}/admin/user/remove',
                    json=remove_input).raise_for_status()

    # Test that other users can use the same email
    member_user_2 = new_user(email='pleb@slackr.com')

    assert member_user['u_id'] != member_user_2['u_id']


def test_user_remove_after_removal_channel(reset, new_user, new_channel,
                                           get_channel_details):
    '''Test that the results of removing a user in regards to channels'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    test_channel = new_channel(admin_user)

    join_input = {
        'token': member_user['token'],
        'channel_id': test_channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/join', json=join_input)

    channel_members = get_channel_details(
        admin_user['token'], test_channel['channel_id'])['all_members']
    assert len(channel_members) == 2

    remove_input = {'token': admin_user['token'], 'u_id': member_user['u_id']}
    requests.delete(f'{BASE_URL}/admin/user/remove',
                    json=remove_input).raise_for_status()

    channel_members = get_channel_details(
        admin_user['token'], test_channel['channel_id'])['all_members']
    assert len(channel_members) == 1


def test_user_remove_after_removal_msgs(reset, new_user, new_channel,
                                        get_channel_details, send_msg):
    '''Test that the results of removing a user in regards to messages'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    test_channel = new_channel(admin_user)

    join_input = {
        'token': member_user['token'],
        'channel_id': test_channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/join', json=join_input)

    channel_members = get_channel_details(
        admin_user['token'], test_channel['channel_id'])['all_members']
    assert len(channel_members) == 2

    send_msg(member_user['token'], test_channel['channel_id'], 'Hello')

    get_msgs_input = {
        'token': admin_user['token'],
        'channel_id': test_channel['channel_id'],
        'start': 0
    }
    channel_msgs = requests.get(f'{BASE_URL}/channel/messages',
                                params=get_msgs_input).json()['messages']
    assert len(channel_msgs) == 1

    remove_input = {'token': admin_user['token'], 'u_id': member_user['u_id']}
    requests.delete(f'{BASE_URL}/admin/user/remove',
                    json=remove_input).raise_for_status()

    # Check that message remains in the channel
    channel_msgs = requests.get(f'{BASE_URL}/channel/messages',
                                params=get_msgs_input).json()['messages']
    assert len(channel_msgs) == 1


def test_user_remove_after_removal_reacts(reset, new_user, new_channel,
                                          get_channel_details, send_msg):
    '''Test that the results of removing a user in regards to reacts'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    test_channel = new_channel(admin_user)

    join_input = {
        'token': member_user['token'],
        'channel_id': test_channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/join', json=join_input)

    channel_members = get_channel_details(
        admin_user['token'], test_channel['channel_id'])['all_members']
    assert len(channel_members) == 2

    test_msg = send_msg(member_user['token'], test_channel['channel_id'],
                        'Hello')

    react_input = {
        'token': member_user['token'],
        'message_id': test_msg['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    get_msgs_input = {
        'token': admin_user['token'],
        'channel_id': test_channel['channel_id'],
        'start': 0
    }
    channel_msgs = requests.get(f'{BASE_URL}/channel/messages',
                                params=get_msgs_input).json()['messages']
    assert len(channel_msgs) == 1
    assert len(channel_msgs[0]['reacts']) == 1

    remove_input = {'token': admin_user['token'], 'u_id': member_user['u_id']}
    requests.delete(f'{BASE_URL}/admin/user/remove',
                    json=remove_input).raise_for_status()

    # Check that message remains in the channel
    channel_msgs = requests.get(f'{BASE_URL}/channel/messages',
                                params=get_msgs_input).json()['messages']
    assert len(channel_msgs) == 1
    assert len(channel_msgs[0]['reacts']) == 1


def test_user_remove_after_removal_token(reset, new_user):
    '''Test that the results of removing a user in regards to the user token'''

    admin_user = new_user(email='admin@slackr.com')
    member_user = new_user(email='pleb@slackr.com')

    create_input = {
        'token': member_user['token'],
        'name': 'Channel',
        'is_public': True
    }
    requests.post(f'{BASE_URL}/channels/create',
                  json=create_input).raise_for_status()

    remove_input = {'token': admin_user['token'], 'u_id': member_user['u_id']}
    requests.delete(f'{BASE_URL}/admin/user/remove',
                    json=remove_input).raise_for_status()

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/channels/create',
                      json=create_input).raise_for_status()
