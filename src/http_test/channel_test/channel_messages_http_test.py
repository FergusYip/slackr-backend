'''
HTTP Tests for the channel_messages function.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_messages_send(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing message send function.
    '''

    user1 = new_user(email='user_1@email.com')
    user2 = new_user(email='user_2@email.com')
    channel = new_channel(user1)

    join_in = {'token': user2['token'], 'channel_id': channel['channel_id']}

    # user2 joins the new channel.
    requests.post(f'{BASE_URL}/channel/join', json=join_in)

    message_in_u1 = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'message': 'hello'
    }

    message_in_u2 = {
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'message': 'hi'
    }

    requests.post(f'{BASE_URL}/message/send', json=message_in_u1)
    requests.post(f'{BASE_URL}/message/send', json=message_in_u2)

    history_in = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_history = requests.get(f'{BASE_URL}/channel/messages',
                                   params=history_in).json()

    assert len(message_history['messages']) == 2
    assert message_history['start'] == 0


def test_message_remove(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing message function after removal.
    '''

    user1 = new_user()
    channel = new_channel(user1)

    message_in_u1 = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'message': 'hello'
    }

    m_id = requests.post(f'{BASE_URL}/message/send', json=message_in_u1).json()

    delete_in = {'token': user1['token'], 'message_id': m_id['message_id']}

    requests.delete(f'{BASE_URL}/message/remove', json=delete_in)

    history_in = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_history = requests.get(f'{BASE_URL}/channel/messages',
                                   params=history_in).json()

    assert len(message_history['messages']) == 0


def test_invalid_id(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing channel messages when invalid channel id is passed.
    '''

    user1 = new_user()
    new_channel(user1)

    history_in = {'token': user1['token'], 'channel_id': -1, 'start': 0}

    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/channel/messages',
                     params=history_in).raise_for_status()


def test_invalid_start(reset, new_user, new_channel, send_msg):  # pylint: disable=W0613
    '''
    Testing channel messages when invalid start is passed.
    '''

    user1 = new_user()
    channel = new_channel(user1)

    send_msg(user1['token'], channel['channel_id'], 'hello')

    history_in = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'start': -1
    }

    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/channel/messages',
                     params=history_in).raise_for_status()


def test_access(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing channel messages for non-member user request.
    '''

    user1 = new_user(email='user_1@email.com')
    user2 = new_user(email='user_2@email.com')
    channel = new_channel(user1)

    message_in_u1 = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'message': 'hello'
    }

    requests.post(f'{BASE_URL}/message/send', json=message_in_u1).json()

    history_in = {
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    # user2 (non-member of channel) requests message history.
    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/channel/messages',
                     params=history_in).raise_for_status()
