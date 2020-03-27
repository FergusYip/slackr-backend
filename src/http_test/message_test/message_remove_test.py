'''
Testing the message_remove functionality.
'''

import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'

# =====================================================
# ========= TESTING MESSAGE REMOVE FUNCTION ===========
# =====================================================

def test_remove_returntype(reset, new_user, new_channel):
    '''
    Testing the return type of the message/remove route.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    test_message = requests.post(f'{BASE_URL}/message/send',
                                 json=message_info).json().raise_for_status

    assert test_message['message_id'] == 1

    # Sending a second message as to not raise an error if no messages exist once one is deleted.
    second_message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message2'
    }

    second_test_message = requests.post(f'{BASE_URL}/message/send',
                                        json=second_message_info).json().raise_for_status

    assert second_test_message['message_id'] == 2

    # Will now get a list of messages in the channel from index 0.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=func_input).json()

    # Now calling the removal function.
    remove_input = {
        'token': user['token'],
        'message_id': message_from_data[0]['message_id']
    }

    remove_return = requests.delete(f'{BASE_URL}/message/remove', json=remove_input).json()

    assert isinstance(remove_return, dict)


def test_remove_message(reset, new_user, new_channel):
    '''
    Testing the return type of the message/remove route.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    test_message = requests.post(f'{BASE_URL}/message/send',
                                 json=message_info).json().raise_for_status

    assert test_message['message_id'] == 1

    # Sending a second message as to not raise an error if no messages exist once one is deleted.
    second_message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message2'
    }

    second_test_message = requests.post(f'{BASE_URL}/message/send',
                                        json=second_message_info).json().raise_for_status

    assert second_test_message['message_id'] == 2

    # Will now get a list of messages in the channel from index 0.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=func_input).json()

    # Now calling the removal function.
    remove_input = {
        'token': user['token'],
        'message_id': message_from_data[0]['message_id']
    }

    requests.delete(f'{BASE_URL}/message/remove', json=remove_input).json()

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=func_input).json()

    # Asser that message with message_id '1' was removed so the 0 index
    # in the channel is message_id '2'. And that only 1 message exists.
    assert len(message_from_data['messages']) == 1
    assert message_from_data[0]['message_id'] == 2


def test_remove_invalid_message(reset, new_user, new_channel):
    '''
    Testing that an error is raised if the channel or message is invalid.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    test_message = requests.post(f'{BASE_URL}/message/send',
                                 json=message_info).json().raise_for_status

    assert test_message['message_id'] == 1

    # Getting a list of messages in the channel.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=func_input).json()

    # Removing an invalid message_id. As index 1 does not exist.
    remove_input = {
        'token': user['token'],
        'message_id': message_from_data[1]['message_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.delete(f'{BASE_URL}/message/remove', json=remove_input).json()


def test_remove_notadmin(reset, new_user, new_channel):
    '''
    Testing that a user that is not admin or server owner will not be able
    to remove messages in the channel, and the function will raise an error.
    '''

    user = new_user()
    second_user = new_user(email='tester@test.com')

    channel = new_channel(user)

    # Have second_user join the channel.
    function_input = {
        'token': second_user['token'],
        'channel_id': channel['channel_id']
    }

    check_dict = requests.post(f'{BASE_URL}/channel/join',
                               json=function_input).json().raise_for_status

    assert isinstance(check_dict, dict)

    # Have user send a message in the channel.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    test_message = requests.post(f'{BASE_URL}/message/send',
                                 json=message_info).json().raise_for_status

    assert test_message['message_id'] == 1

    # Get a list of all the messages from index 0 in the channel.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=func_input).json()

    # second_user is not admin or server owner.
    remove_input = {
        'token': second_user['token'],
        'message_id': message_from_data[0]['message_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.delete(f'{BASE_URL}/message/remove', json=remove_input).json()


def test_remove_invalid_token(reset, new_user, new_channel, invalid_token):
    '''
    Testing that attempting to remove a message with an invalid token will
    raise an error.
    '''

    user = new_user(email='notusedyet@test.com')
    channel = new_channel(user)

    # Have user send a message in the channel.
    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    test_message = requests.post(f'{BASE_URL}/message/send',
                                 json=message_info).raise_for_status()

    assert test_message['message_id'] == 1

    # Get a list of all the messages from index 0 in the channel.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', json=func_input).json()

    # While the message exists at index 0, the token is invalid.
    remove_input = {
        'token': invalid_token,
        'message_id': message_from_data[0]['message_id']
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/remove',
                      json=remove_input).raise_for_status()
