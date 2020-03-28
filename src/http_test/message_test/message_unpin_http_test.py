'''
Testing the message_unpin functionality.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'

# =====================================================
# ========== TESTING MESSAGE UNPIN FUNCTION ===========
# =====================================================

def test_unpin_return(reset, new_user, new_channel):
    '''
    Testing the return value of the message_unpin function.
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

    # Pin the message as user.
    func_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    requests.post(f'{BASE_URL}/message/pin', json=func_input)

    # Unpin the message as user.
    unpin_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    unpin_return = requests.post(f'{BASE_URL}/message/unpin', json=unpin_input)

    assert isinstance(unpin_return, dict)


def test_unpin_message(reset, new_user, new_channel):
    '''
    Testing the average case functionality of the message_unpin function.
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

    # Initially pinning the message as user.
    pin_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    requests.post(f'{BASE_URL}/message/pin', json=pin_input)

    # Get a list of all messages in the channel.
    function_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=function_input).json()
    assert message_from_data['messages'][0]['is_pinned']

    unpin_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }
    requests.post(f'{BASE_URL}/message/unpin', json=unpin_input)

    # Update the list of messages in the channel.
    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=function_input).json()
    assert not message_from_data['messages'][0]['is_pinned']


def test_unpin_invalid_message(reset, new_user):
    '''
    Testing that attempting to unpin an invalid message will result
    in an error.
    '''

    user = new_user()

    # Message with ID of 1 does not exist.
    unpin_input = {
        'token': user['token'],
        'message_id': 1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/unpin', json=unpin_input).raise_for_status()


def test_unpin_notadmin(reset, new_user, new_channel):
    '''
    Testing that a non-admin cannot unpin messages. This will result in
    an error.
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

    # Initially pinning the message as user.
    pin_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    requests.post(f'{BASE_URL}/message/pin', json=pin_input)

    unpin_input = {
        'token': second_user['token'],
        'message_id': message_info['message_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/unpin', json=unpin_input).raise_for_status()


def test_unpin_notpinned(reset, new_user, new_channel):
    '''
    Testing that attempting to unpin a message that is not yet pinned will
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

    # Attempting to unpin the non-pinned message.
    unpin_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/unpin', json=unpin_input).raise_for_status()


def test_unpin_notinchannel(reset, new_user, new_channel):
    '''
    Testing that if an admin has left the channel, they are no longer able
    to unpin messages, resulting in an error being raised.
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

    # Initially pinning the message as user.
    pin_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    requests.post(f'{BASE_URL}/message/pin', json=pin_input)

    # Leave the channel as user.
    leave_input = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/leave', json=leave_input)

    # Attempting to unpin after leaving the channel.
    unpin_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/unpin', json=unpin_input).raise_for_status()


def test_unpin_invalid_token(reset, new_user, new_channel):
    '''
    Testing that if there is an attempt to unpin a message with an invalid
    token, an error will be raised.
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

    pin_input = {
        'token': user['token'],
        'message_id': message_info['message_id']
    }

    requests.post(f'{BASE_URL}/message/pin', json=pin_input)

    # Logging the user out.
    token = user['token']
    requests.post(f"{BASE_URL}/auth/logout", json={'token': token})

    unpin_input = {
        'token': token,
        'message_id': message_info['message_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/unpin', json=unpin_input).raise_for_status()
