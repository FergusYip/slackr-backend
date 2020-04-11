'''
Testing the functionality of the message_edit function.

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
# ========== TESTING MESSAGE EDIT FUNCTION ============
# =====================================================

def test_edit_return(reset, new_user, new_channel):
    '''
    Testing the return type of the message_edit route. Should result
    in an empty dictionary.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending a message as user.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    requests.post(f'{BASE_URL}/message/send',
                  json=message_info)

    edit_input = {
        'token': user['token'],
        'message_id': 1,
        'message': 'New message'
    }

    return_type = requests.put(f'{BASE_URL}/message/edit',
                               json=edit_input).json()

    assert isinstance(return_type, dict)


def test_edit_message(reset, new_user, new_channel):
    '''
    Testing an average use case of message_edit.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending a message as user.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    requests.post(f'{BASE_URL}/message/send',
                  json=message_info).json()

    # Getting a list of messages.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=func_input).json()

    # Assert the message sent correctly.
    assert message_from_data['messages'][0]['message'] == 'Message'

    # Change the message.
    edit_input = {
        'token': user['token'],
        'message_id': message_from_data['messages'][0]['message_id'],
        'message': 'Edited Message'
    }

    requests.put(f'{BASE_URL}/message/edit',
                 json=edit_input).json()

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=func_input).json()

    # Assert the message has been updated successfully.
    assert message_from_data['messages'][0]['message'] == 'Edited Message'

def test_edit_invalid_message(reset, new_user, new_channel):
    '''
    Testing that attempting to edit an invalid message_id will raise an error.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending a message as user.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    requests.post(f'{BASE_URL}/message/send',
                  json=message_info).json()

    # Message in index position 1 does not exist. (only index 0 does).
    edit_input = {
        'token': user['token'],
        'message_id': 2,
        'message': 'Hello World'
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/message/edit',
                     json=edit_input).raise_for_status()

def test_edit_message_length(reset, new_user, new_channel):
    '''
    Testing that a message with a length greater than 1,000 characters
    will raise an error.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending a message.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    requests.post(f'{BASE_URL}/message/send',
                  json=message_info).json()

    # Getting a list of messages.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=func_input).json()

    edit_input = {
        'token': user['token'],
        'message_id': message_from_data['messages'][0]['message_id'],
        'message': 'i' * 1001
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/message/edit',
                     json=edit_input).raise_for_status()


def test_edit_privileges(reset, new_user, new_channel):
    '''
    Testing that a user that does not have the same u_id as the u_id in the
    message information will raise an error if they attempt to edit message.
    '''

    user = new_user()
    second_user = new_user(email='tester@test.com')

    channel = new_channel(user)

    # Joining the channel as the second_user.
    function_input = {
        'token': second_user['token'],
        'channel_id': channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/join', json=function_input)

    # Sending a message as user.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    requests.post(f'{BASE_URL}/message/send', json=message_info)

    # Getting a list of messages.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=func_input).json()

    # Attempting to edit the message as the second user.
    edit_input = {
        'token': second_user['token'],
        'message_id': message_from_data['messages'][0]['message_id'],
        'message': 'New message'
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/message/edit',
                     json=edit_input).raise_for_status()

def test_edit_admin(reset, new_user, new_channel):
    '''
    Testing that a server admin or channel owner is able to edit other
    user's messages.
    '''

    user = new_user()
    second_user = new_user(email='tester@test.com')

    channel = new_channel(user)

    # Joining the channel as the second user.
    function_input = {
        'token': second_user['token'],
        'channel_id': channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/join', json=function_input)

    # Sending a message as the second user.
    message_info = {
        'token': second_user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    requests.post(f'{BASE_URL}/message/send', json=message_info)

    # Getting a list of messages in the channel.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=func_input).json()

    edit_input = {
        'token': user['token'],
        'message_id': message_from_data['messages'][0]['message_id'],
        'message': 'New message'
    }

    # Admin should be able to successfully edit another user's message.
    requests.put(f'{BASE_URL}/message/edit', json=edit_input)

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=func_input).json()

    assert message_from_data['messages'][0]['message'] == 'New message'


def test_edit_nolength(reset, new_user, new_channel):
    '''
    Testing that editing a message to have a length of zero characters will
    remove the message from the channel.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending one message in the channel.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    requests.post(f'{BASE_URL}/message/send', json=message_info)

    # Sending a second message in the channel to not raise an error with
    # channel_messages.
    message_info['message'] = '2nd message'

    requests.post(f'{BASE_URL}/message/send', json=message_info)

    # Getting a list of messages in the channel.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=func_input).json()

    # Editing the message with a string of zero characters.
    edit_input = {
        'token': user['token'],
        'message_id': message_from_data['messages'][0]['message_id'],
        'message': ''
    }

    requests.put(f'{BASE_URL}/message/edit', json=edit_input)

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=func_input).json()

    # The edited message should have been deleted, leaving only one message.
    assert len(message_from_data['messages']) == 1
    assert message_from_data['messages'][0]['message'] == '2nd message'


def test_invalid_token(reset, new_user, new_channel):
    '''
    Testing that calling the message_edit function with an invalid token
    will raise an error.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending one message in the channel.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    requests.post(f'{BASE_URL}/message/send', json=message_info)

    # Getting a list of the messages in the channel.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=func_input).json()

    # Logging the user out, rendering the token invalid.
    token = user['token']
    requests.post(f"{BASE_URL}/auth/logout", json={'token': token})

    edit_input = {
        'token': token,
        'message_id': message_from_data['messages'][0]['message_id'],
        'message': 'New message'
    }

    with pytest.raises(requests.HTTPError):
        requests.put(f'{BASE_URL}/message/edit',
                     json=edit_input).raise_for_status()
