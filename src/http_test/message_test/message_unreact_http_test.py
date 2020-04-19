'''
Testing the message_unreact functionality.

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
# ========= TESTING MESSAGE UNREACT FUNCTION ==========
# =====================================================


def test_unreact_returntype(reset, new_user, new_channel):
    '''
    Testing the return type of the message_unreact route.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send',
                                 json=message_input).json()

    # Reacting to the message with react_id of 1.
    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    # Removing the reaction.
    unreact_info = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    unreact_return = requests.post(f'{BASE_URL}/message/unreact',
                                   json=unreact_info).json()

    assert isinstance(unreact_return, dict)


def test_unreact_message(reset, new_user, new_channel):
    '''
    Testing that the function removes a reaction properly and that it removes
    the reaction from the list of reactions on that message.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send',
                                 json=message_input).json()

    # Adding a reaction to the message.
    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    # Getting a list of messages to check that the user has reacted.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages',
                                     params=func_input).json()
    assert message_from_data['messages'][0]['reacts'][0]['u_ids'][0] == user[
        'u_id']

    unreact_info = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/unreact', json=unreact_info)

    message_from_data = requests.get(f'{BASE_URL}/channel/messages',
                                     params=func_input).json()

    # Assert there are no values in the list of reactions.
    assert not message_from_data['messages'][0]['reacts']


def test_unreact_multiple_users(reset, new_user, new_channel):
    '''
    Testing that the function removes a reaction properly and that it removes
    the user's u_id from the list of u_ids that have reacted.
    '''

    user = new_user()
    second_user = new_user(email='tester@test.com')
    channel = new_channel(user)

    # Have second_user join the channel.
    function_input = {
        'token': second_user['token'],
        'channel_id': channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/join', json=function_input)

    # Sending the first message in a channel as user.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send',
                                 json=message_input).json()

    # Adding a reaction to the message as user.
    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    # Adding a reaction to the message as second_user.
    react_input['token'] = second_user['token']
    requests.post(f'{BASE_URL}/message/react', json=react_input)

    # Getting a list of messages to check that the users has reacted.
    func_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages',
                                     params=func_input).json()

    assert len(message_from_data['messages'][0]['reacts'][0]['u_ids']) == 2

    # Unreact as user.
    unreact_info = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/unreact', json=unreact_info)

    # Update the list of messages in the channel.
    message_from_data = requests.get(f'{BASE_URL}/channel/messages',
                                     params=func_input).json()

    # Assert there remains only one reaction type.
    assert len(message_from_data['messages'][0]['reacts']) == 1
    # Assert the zero indexed react u_id is now the second_user.
    assert message_from_data['messages'][0]['reacts'][0]['u_ids'][
        0] == second_user['u_id']

    # Unreacting as second_user.
    unreact_info['token'] = second_user['token']
    requests.post(f'{BASE_URL}/message/unreact', json=unreact_info)

    # Updating the list of messages in the channel.
    message_hello = requests.get(f'{BASE_URL}/channel/messages',
                                 params=func_input).json()
    # Assert that the reaction was removed as there were no u_ids in the react.
    assert len(message_hello['messages'][0]['reacts']) == 0


def test_unreact_invalid_message(reset, new_user, new_channel):
    '''
    Testing that attempting to unreact to an invalid message will raise an error.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel as user.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send',
                                 json=message_input).json()

    # Add a reaction to the message.
    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    # Attempt to unreact to a message_id that does not exist.
    # (ID #2 does not exist)
    unreact_info = {'token': user['token'], 'message_id': 2, 'react_id': 1}
    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/unreact',
                      json=unreact_info).raise_for_status()


def test_unreact_notchannelmember(reset, new_user, new_channel):
    '''
    Testing that attempting to unreact to a message in a channel the user is
    not a member of will raise an error.
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

    message_info = requests.post(f'{BASE_URL}/message/send',
                                 json=message_input).json()

    # Reacting to the message as second_user.
    react_input = {
        'token': second_user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    # Leave the channel as second_user.
    leave_input = {
        'token': second_user['token'],
        'channel_id': channel['channel_id']
    }

    requests.post(f'{BASE_URL}/channel/leave', json=leave_input)

    # Assert the reaction still exists.
    function_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages',
                                     params=function_input).json()
    assert message_from_data['messages'][0]['reacts'][0]['u_ids'][
        0] == second_user['u_id']

    # Attempting to unreact as second_user should raise an error.
    unreact_info = {
        'token': second_user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/unreact',
                      json=unreact_info).raise_for_status()


def test_unreact_invalid_reactid(reset, new_user, new_channel):
    '''
    Testing that attempting to unreact with an invalid react_id will raise an
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

    message_info = requests.post(f'{BASE_URL}/message/send',
                                 json=message_input).json()

    # Reacting to the message with react_id of 1.
    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    # Attempting to unreact with react_id of 2.
    unreact_info = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 2
    }
    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/unreact',
                      json=unreact_info).raise_for_status()


def test_notyetreacted(reset, new_user, new_channel):
    '''
    Testing that attempting to unreact to a message that the user has not yet
    reacted to will raise an error.
    '''

    user = new_user()
    channel = new_channel(user)

    # Sending the first message in a channel.
    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_info = requests.post(f'{BASE_URL}/message/send',
                                 json=message_input).json()

    # Attempting to unreact to a message that the user has not yet reacted to.
    unreact_info = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/unreact',
                      json=unreact_info).raise_for_status()


def test_uid_not_reacted(reset, new_user, new_channel):
    '''
    Testing that attempting to unreact to a message that exists and has
    reactions, as a user that has not yet reacted yet will raise an error.
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

    message_info = requests.post(f'{BASE_URL}/message/send',
                                 json=message_input).json()

    # Reacting to the message as user.
    react_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }

    requests.post(f'{BASE_URL}/message/react', json=react_input)

    # Attempting to unreact as second_user, who has not reacted yet.
    unreact_info = {
        'token': second_user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }
    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/unreact',
                      json=unreact_info).raise_for_status()


def test_unreact_invalid_token(reset, new_user, new_channel):
    '''
    Testing that attempting to call message_unreact with an invalid token will
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

    message_info = requests.post(f'{BASE_URL}/message/send',
                                 json=message_input).json()

    func_input = {
        'token': user['token'],
        'message_id': message_info['message_id'],
        'react_id': 1
    }
    requests.post(f'{BASE_URL}/message/react', json=func_input)

    # Logging the user out.
    token = user['token']
    requests.post(f"{BASE_URL}/auth/logout", json={'token': token})

    unreact_info = {
        'token': token,
        'message_id': message_info['message_id'],
        'react_id': 1
    }
    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/unreact',
                      json=unreact_info).raise_for_status()
