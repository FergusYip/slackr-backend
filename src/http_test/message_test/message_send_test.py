'''
Testing the message_send functionality.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'

# =====================================================
# ========== TESTING MESSAGE SEND FUNCTION ============
# =====================================================

def test_send_returntype(reset, new_user, new_channel):
    '''
    Testing the return type of the message/send route.
    '''

    user = new_user()
    channel = new_channel(user)

    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    test_message = requests.post(f'{BASE_URL}/message/send', json=message_info).json()

    assert isinstance(test_message, dict)
    assert isinstance(test_message['message_id'], int)


def test_send_message(reset, new_user, new_channel):
    '''
    Testing that the correct message string sent.
    '''

    user = new_user()
    channel = new_channel(user)

    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    test_message = requests.post(f'{BASE_URL}/message/send',
                                 json=message_info).json().raise_for_status

    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=func_input).json()

    assert message_from_data[0]['message_id'] == test_message['message_id']


def test_message_user(reset, new_user, new_channel):
    '''
    Testing that the message was appended appended with the authorized user's
    u_id.
    '''

    user = new_user()
    channel = new_channel(user)

    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    test_message = requests.post(f'{BASE_URL}/message/send',
                                 json=message_info).json().raise_for_status

    assert test_message['message_id'] == 1

    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=func_input).json()

    assert message_from_data[0]['u_id'] == user['u_id']


def test_send_reacts(reset, new_user, new_channel):
    '''
    Testing that the list of reactions is empty after a message is sent.
    '''

    user = new_user()
    channel = new_channel(user)

    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    test_message = requests.post(f'{BASE_URL}/message/send',
                                 json=message_info).json().raise_for_status

    assert test_message['message_id'] == 1

    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=func_input).json()

    assert len(message_from_data[0]['reacts']) == 0


def test_send_pinned(reset, new_user, new_channel):
    '''
    Testing that the pinned status is False after a message is sent.
    '''

    user = new_user()
    channel = new_channel(user)

    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    test_message = requests.post(f'{BASE_URL}/message/send',
                                 json=message_info).json().raise_for_status

    assert test_message['message_id'] == 1

    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=func_input).json()

    assert not message_from_data[0]['is_pinned']


def test_send_long_message(reset, new_user, new_channel):
    '''
    Testing that a message over 1,000 characters raises an error.
    '''

    user = new_user()
    channel = new_channel(user)

    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'i' * 1001
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/send',
                      json=message_info).raise_for_status()


def test_send_short_message(reset, new_user, new_channel):
    '''
    Testing that a message of 0 characters raises an error.
    '''

    user = new_user()
    channel = new_channel(user)

    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': ''
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/send',
                      json=message_info).raise_for_status()


def test_send_invalid_channel(reset, new_user):
    '''
    Testing that a message raises an error if the user attempts to append the
    message to an invalid channel.
    '''

    user = new_user()

    message_info = {
        'token': user['token'],
        'channel_id': 1,
        'message': 'Message'
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/send',
                      json=message_info).raise_for_status()

def test_send_channel_notmember(reset, new_user, new_channel):
    '''
    Testing that a message raises an error if a user attempts to append to a
    channel they are not a member of.
    '''

    user = new_user()

    channel = new_channel(user)

    user2 = new_user(email='valid2@email.com')

    message_info = {
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/send',
                      json=message_info).raise_for_status()


def test_message_invalid_token(reset, new_user, new_channel, invalid_token):
    '''
    Testing that attempting to send a message with an invalid token will
    raise an error.
    '''

    user = new_user(email='notusedyet@test.com')
    channel = new_channel(user)

    message_info = {
        'token': invalid_token,
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/send',
                      json=message_info).raise_for_status()
