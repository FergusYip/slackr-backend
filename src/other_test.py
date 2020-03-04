import pytest
import auth
import channel
import channels
import message
import other
import user
from error import AccessError


def test_users_all(test_user):
    test_user_profile = user.user_profile(test_user['token'],
                                          test_user['u_id'])['user']
    all_users = other.users_all(test_user['token'])

    assert test_user_profile in all_users['users']


def test_users_all_invalid_token(invalid_token):
    with pytest.raises(AccessError):
        other.users_all(invalid_token)


def test_search_no_channel(test_user):
    assert len(other.search(test_user['token'], '')['messages']) == 0


def test_search_empty_channel(test_user, test_channel):
    channel.channel_join(test_user['token'], test_channel['channel_id'])
    assert len(other.search(test_user['token'], '')['messages']) == 0


def test_search_single_channel(test_user, test_channel):
    channel.channel_join(test_user['token'], test_channel['channel_id'])
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Hello world!')

    msg_in_channel = channel.channel_messages(test_user['token'],
                                              test_channel['channel_id'],
                                              0)['messages'][0]
    msg_in_search = other.search(test_user['token'], 'Hello')['messages'][0]

    assert msg_in_channel == msg_in_search


def test_search_multiple_messages(test_user, test_channel):
    channel.channel_join(test_user['token'], test_channel['channel_id'])

    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Alpha')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Bravo')
    message.message_send(test_user['token'], test_channel['channel_id'],
                         'Charlie')

    assert len(other.search(test_user['token'], 'a')['messages']) == 3
    assert len(other.search(test_user['token'], 'b')['messages']) == 1
    assert len(other.search(test_user['token'], 'Romeo')['messages']) == 0


def test_search_multiple_channels(test_user):
    ch1 = channels.channels_create(test_user['token'], 'Channel', True)
    channel.channel_join(test_user['token'], ch1['channel_id'])
    message.message_send(test_user['token'], ch1['channel_id'], 'Channel 1')

    ch2 = channels.channels_create(test_user['token'], 'Channel', True)
    channel.channel_join(test_user['token'], ch1['channel_id'])
    message.message_send(test_user['token'], ch2['channel_id'], 'Channel 2')

    ch3 = channels.channels_create(test_user['token'], 'Channel', True)
    channel.channel_join(test_user['token'], ch1['channel_id'])
    message.message_send(test_user['token'], ch3['channel_id'], 'Channel 3')

    assert len(other.search(test_user['token'], 'Channel')['messages']) == 3


def test_search_case_insensitive(test_user, test_channel):
    channel.channel_join(test_user['token'], test_channel['channel_id'])
    msg = message.message_send(test_user['token'], test_channel['channel_id'],
                               'Hello world!')
    msg_in_channel = channel.channel_messages(test_user['token'],
                                              test_channel['channel_id'],
                                              0)['messages'][0]
    msg_in_search = other.search(test_user['token'], 'hello')['messages'][0]
    assert msg_in_channel == msg_in_search


def test_search_invalid_token(invalid_token):
    with pytest.raises(AccessError):
        other.search(invalid_token, '')
