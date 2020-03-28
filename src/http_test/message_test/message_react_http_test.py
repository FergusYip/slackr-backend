'''
Testing the message_react functionality.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'

# =====================================================
# ========== TESTING MESSAGE REACT FUNCTION ===========
# =====================================================

def test_react_returntype(reset, new_user, new_channel):
    '''
    Testing the return type of the message_react route.
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

    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    react_return = requests.post(f'{BASE_URL}/message/react', json=react_input).json()

    assert isinstance(react_return, dict)


def test_add_react(reset, new_user, new_channel):
    '''
    Testing that the function adds a reaction properly and that it appends the
    user's u_id to the list of u_ids that have reacted.
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

    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=func_input).json()

    assert len(message_from_data['messages'][0]['reacts']) == 1
    assert message_from_data['messages'][0]['reacts'][0]['u_ids'][0] == user['u_id']

def test_react_invalid_message(reset, new_user, new_channel):
    '''
    Testing that attempting to react to an invalid message will raise an error.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    requests.post(f'{BASE_URL}/message/send', json=message_input)

    # Message ID of 2 does not exist. (only ID #1 exists)
    react_input = {
        'token': user['token'],
        'message_id': 2,
        'react_id': 1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/react', json=react_input).raise_for_status()


def test_react_notinchannel(reset, new_user, new_channel):
    '''
    Testing that if the user is not in the channel, an error will be raised
    if they attempt to react to a message.
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

    # Attempt to react.
    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/react', json=react_input).raise_for_status()


def test_invalid_reactid(reset, new_user, new_channel):
    '''
    Testing that attempting to react with an invalid react_id will raise an
    error.
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

    # React ID of 2 does not exist. (only ID #1 exists)
    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 2
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/react', json=react_input).raise_for_status()


def test_react_already_reacted(reset, new_user, new_channel):
    '''
    Testing that attempting to react to a message you have already reacted to
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

    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    # If the user attempts to react again, it should raise an error.
    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/react', json=react_input).raise_for_status()


def test_react_multiple_users(reset, new_user, new_channel):
    '''
    Testing the case where there are multiple reactions to ensure u_ids
    are appended in the correct order and that the state of the number of
    reactions is unchanged, just with more u_ids.
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

    # Sending the first message in a channel.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send', json=message_input).json()

    # Making user react to the message.
    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    # Making second_user react to the message.
    react_input['token'] = second_user['token']

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    # Get a list of all messages in the channel (to see the reactions).
    function_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=function_input).json()

    # Should still only be one reaction, just with multiple IDs.
    assert len(message_from_data['messages'][0]['reacts']) == 1
    # Should append u_ids in the order that they reacted.
    assert message_from_data['messages'][0]['reacts'][0]['u_ids'][0] == user['u_id']
    assert message_from_data['messages'][0]['reacts'][0]['u_ids'][1] == second_user['u_id']


def test_react_invalid_token(reset, new_user, new_channel):
    '''
    Testing that attempting to call message_react with an invalid token will
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

    # Logging the user out.
    token = user['token']
    requests.post(f"{BASE_URL}/auth/logout", json={'token': token})

    func_input = {
        'token': token,
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/react', json=func_input).raise_for_status()
