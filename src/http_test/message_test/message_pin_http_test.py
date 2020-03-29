'''
Testing the message_pin functionality.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'

# =====================================================
# =========== TESTING MESSAGE PIN FUNCTION ============
# =====================================================

def test_pin_returntype(reset, new_user, new_channel):
    '''
    Testing the return value of the message_pin function.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send', json=message_input).json()

    func_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    pin_return = requests.post(f'{BASE_URL}/message/pin', json=func_input).json()

    assert isinstance(pin_return, dict)


def test_pin_message(reset, new_user, new_channel):
    '''
    Testing the average case functionality of message_pin function.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send', json=message_input).json()

    func_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    requests.post(f'{BASE_URL}/message/pin', json=func_input)

    # Get a list of all messages in the channel.
    function_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=function_input).json()
    assert message_from_data['messages'][0]['is_pinned']


def test_pin_invalid_message(reset, new_user):
    '''
    Testing that attempting to pin an invalid message will raise an error.
    '''

    user = new_user()

    func_input = {
        'token': user['token'],
        'message_id': 1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/pin', json=func_input).raise_for_status()



def test_pin_notadmin(reset, new_user, new_channel):
    '''
    Testing that attempting to pin a message as a member that is not an
    admin will raise an error.
    '''

    user = new_user()
    second_user = new_user(email='tester@test.com')

    channel = new_channel(user)

    # Have second_user join the channel.
    func_input = {
        'token': second_user['token'],
        'channel_id': channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/join', json=func_input)

    # Sending the first message in the channel as user.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send', json=message_input).json()

    # Attempting to pin the message as a non-admin.
    function_input = {
        'token': second_user['token'],
        'message_id': message_info['message_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/pin', json=function_input).raise_for_status()



def test_pin_already_pinned(reset, new_user, new_channel):
    '''
    Testing that attempting to pin a message that is already pinned will
    raise an error.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send', json=message_input).json()
    # Pin the message.
    func_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    requests.post(f'{BASE_URL}/message/pin', json=func_input)

    # Attempting to pin the message again will result in an error being raised.
    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/pin', json=func_input).raise_for_status()


def test_pin_admin_leave_channel(reset, new_user, new_channel):
    '''
    Testing that if an admin leaves the channel, they are no longer able to
    pin messages, thus resulting in an error being raised.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send', json=message_input).json()

    # Leave the channel as user.
    leave_input = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/leave', json=leave_input)

    # Attempt to pin the message, raising an error.
    func_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/pin', json=func_input).raise_for_status()


def test_pin_invalid_token(reset, new_user, new_channel):
    '''
    Testing that attempting to call message_pin with an invalid token
    will raise an error.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send', json=message_input).json()

    # Logging the user out.
    token = user['token']
    requests.post(f"{BASE_URL}/auth/logout", json={'token': token})

    func_input = {
        'token': token,
        'message_id': message_info['message_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/pin', json=func_input).raise_for_status()
