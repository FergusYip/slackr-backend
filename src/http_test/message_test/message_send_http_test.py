'''
Testing the message_send functionality.

Parameters:
    reset: Reset is a function defined in conftest.py that restores all values
           in the data_store back to being empty.
    new_user: A function defined in conftest.py that will create a new user based on
              default values that can be specified. Returns the u_id and token.
    new_channel: A function defined in conftest.py that will create a new channel based on
              default values that can be specified. Returns the channel_id.
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

    test_message = requests.post(f'{BASE_URL}/message/send',
                                 json=message_info).json()

    assert isinstance(test_message, dict)
    assert isinstance(test_message['message_id'], int)


def test_send_message(reset, new_user, new_channel):
    '''
    Testing that the correct message id was allocated.
    '''

    user = new_user()
    channel = new_channel(user)

    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    test_message = requests.post(f'{BASE_URL}/message/send',
                                 json=message_info).json()

    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages',
                                     params=func_input).json()

    assert message_from_data['messages'][0]['message_id'] == test_message[
        'message_id']


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

    requests.post(f'{BASE_URL}/message/send', json=message_info)

    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages',
                                     params=func_input).json()

    assert message_from_data['messages'][0]['u_id'] == user['u_id']


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

    requests.post(f'{BASE_URL}/message/send', json=message_info)

    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages',
                                     params=func_input).json()

    assert not message_from_data['messages'][0]['reacts']


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

    requests.post(f'{BASE_URL}/message/send', json=message_info)

    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages',
                                     params=func_input).json()

    assert not message_from_data['messages'][0]['is_pinned']


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


def test_message_invalid_token(reset, new_user, new_channel):
    '''
    Testing that attempting to send a message with an invalid token will
    raise an error.
    '''

    user = new_user()
    channel = new_channel(user)

    token = user['token']
    requests.post(f"{BASE_URL}/auth/logout", json={'token': token})

    message_info = {
        'token': token,
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/send',
                      json=message_info).raise_for_status()
