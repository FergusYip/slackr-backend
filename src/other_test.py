import pytest
import auth
import channel
import channels
import message
import other
import user
from error import AccessError


def test_users_all_single_user(test_user):
    '''Test that a single user profile is returned by user_all'''

    test_user_profile = user.user_profile(test_user['token'],
                                          test_user['u_id'])['user']
    all_users = other.users_all(test_user['token'])

    assert test_user_profile in all_users['users']


def test_users_all_multiple_users(new_user):
    '''Test that user_all returns the number of registered users'''

    user_1 = new_user('user_1@email.com')
    assert len(other.users_all(user_1['token'])['users']) == 1

    user_2 = new_user('user_2@email.com')
    assert len(other.users_all(user_2['token'])['users']) == 2

    user_3 = new_user('user_3@email.com')
    assert len(other.users_all(user_3['token'])['users']) == 3


def test_users_all_invalid_token(invalid_token):
    '''Test user_all with invalid token'''

    with pytest.raises(AccessError):
        other.users_all(invalid_token)


def test_search_no_channel(test_user):
    '''Test search function when there is no channel'''

    assert len(other.search(test_user['token'], '')['messages']) == 0


def test_search_empty_channel(test_user, make_join_channel):
    '''Test search function when channel has no messages'''

    test_channel = make_join_channel(test_user, 'Channel')
    assert len(other.search(test_user['token'], '')['messages']) == 0


def test_search_return_type(test_user, make_join_channel):
    '''Test the types of values returned by search'''

    test_channel = make_join_channel(test_user, 'Channel')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Hello world!')

    results = other.search(test_user['token'], 'Hello')['messages'][0]
    assert isinstance(results, dict)
    assert isinstance(results['message_id'], int)
    assert isinstance(results['u_id'], int)
    assert isinstance(results['message'], str)
    assert isinstance(results['time_created'], int)


def test_search_single_channel(test_user, make_join_channel):
    '''Test that the sole message is returned by search'''

    test_channel = make_join_channel(test_user, 'Channel')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Hello world!')

    msg_in_channel = channel.channel_messages(test_user['token'],
                                              test_channel['channel_id'],
                                              0)['messages'][0]
    msg_in_search = other.search(test_user['token'], 'Hello')['messages'][0]

    assert msg_in_channel == msg_in_search


def test_search_multiple_messages(test_user, make_join_channel):
    '''Test search with multiple unique messages'''

    test_channel = make_join_channel(test_user, 'Channel')

    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Alpha')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Bravo')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Charlie')

    assert len(other.search(test_user['token'], 'a')['messages']) == 3
    assert len(other.search(test_user['token'], 'b')['messages']) == 1
    assert len(other.search(test_user['token'], 'Romeo')['messages']) == 0


def test_search_multiple_channels(test_user, make_join_channel):
    '''Test that search works on multiple channels'''

    ch1 = make_join_channel(test_user, 'Channel 1')
    message.message_send(test_user['token'], ch1['channel_id'], 'Channel 1')

    ch2 = make_join_channel(test_user, 'Channel 2')
    message.message_send(test_user['token'], ch2['channel_id'], 'Channel 2')

    ch3 = make_join_channel(test_user, 'Channel 3')
    message.message_send(test_user['token'], ch3['channel_id'], 'Channel 3')

    assert len(other.search(test_user['token'], 'Channel')['messages']) == 3


def test_search_unauthorised_channels(new_user, make_join_channel):
    '''Test that users cannot search unauthorised channels'''

    tom = new_user('tom@email.com')

    jerry = new_user('jerry@email.com')
    mice_ch = make_join_channel(jerry, 'Mice Only')

    message.message_send(jerry['token'], mice_ch['channel_id'],
                         'Tom can\'t see this')

    assert len(other.search(jerry['token'], '')['messages']) == 1
    assert len(other.search(tom['token'], '')['messages']) == 0


def test_search_case_insensitive(test_user, make_join_channel):
    '''Test that query string is not case sensitive'''

    test_channel = make_join_channel(test_user, 'Channel')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Hello world!')
    msg_in_channel = channel.channel_messages(test_user['token'],
                                              test_channel['channel_id'],
                                              0)['messages'][0]
    msg_in_search = other.search(test_user['token'], 'hello')['messages'][0]
    assert msg_in_channel == msg_in_search


def test_search_invalid_token(invalid_token):
    '''Test search function with invalid token'''

    with pytest.raises(AccessError):
        other.search(invalid_token, '')
