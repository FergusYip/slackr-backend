'''
HTTP Tests for the channel_messages function.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_messages_send(reset, new_user, new_channel):
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


def test_messages_react(reset, new_user, new_channel, send_msg):
    '''
    Testing message send function.
    '''

    user = new_user(email='user_1@email.com')
    channel = new_channel(user)

    msg = send_msg(user['token'], channel['channel_id'], 'hello')

    react_input = {
        'token': user['token'],
        'message_id': msg['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    messages_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    channel_messages = requests.get(f'{BASE_URL}/channel/messages',
                                    params=messages_input).json()

    assert len(channel_messages['messages']) == 1
    assert channel_messages['start'] == 0

    assert len(channel_messages['messages'][0]['reacts']) == 1

    react = channel_messages['messages'][0]['reacts'][0]
    assert react['react_id'] == 1


def test_message_remove(reset, new_user, new_channel):
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


def test_invalid_id(reset, new_user, new_channel):
    '''
    Testing channel messages when invalid channel id is passed.
    '''

    user1 = new_user()
    new_channel(user1)

    history_in = {'token': user1['token'], 'channel_id': -1, 'start': 0}

    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/channel/messages',
                     params=history_in).raise_for_status()


def test_invalid_start(reset, new_user, new_channel, send_msg):
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


def test_access(reset, new_user, new_channel):
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


def test_messages_insufficient_params(reset):
    '''Test input of invalid parameters into messages'''

    with pytest.raises(requests.HTTPError):
        requests.get(f"{BASE_URL}/channel/messages",
                     params={}).raise_for_status()
