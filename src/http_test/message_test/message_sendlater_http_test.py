'''
Testing the message_sendlater functionality. Majority of error tests
are performed within the message_send function, which is called within
the mesage_sendlater function.

Parameters:
    reset: Reset is a function defined in conftest.py that restores all values
           in the data_store back to being empty.
    new_user: A function defined in conftest.py that will create a new user based on
              default values that can be specified. Returns the u_id and token.
    new_channel: A function defined in conftest.py that will create a new channel based on
              default values that can be specified. Returns the channel_id.
'''

from time import sleep
from datetime import datetime, timezone
import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'

# =====================================================
# ======== TESTING MESSAGE SENDLATER FUNCTION =========
# =====================================================

def test_sendlater_return(reset, new_user, new_channel):
    '''
    Testing the return value of the message_sendlater function.
    '''
    user = new_user()
    channel = new_channel(user)

    time_now = int(datetime.now(timezone.utc).timestamp())
    time_to_send = time_now + 2

    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message',
        'time_sent': time_to_send
    }

    message_info = requests.post(f'{BASE_URL}/message/sendlater', json=message_input).json()

    assert isinstance(message_info, dict)
    assert isinstance(message_info['message_id'], int)


def test_sendlater_message(reset, new_user, new_channel):
    '''
    Testing the average case functionality of the message_sendlater function.
    '''

    user = new_user()
    channel = new_channel(user)

    time_now = int(datetime.now(timezone.utc).timestamp())
    time_to_send = time_now + 2

    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message',
        'time_sent': time_to_send
    }

    message_info = requests.post(f'{BASE_URL}/message/sendlater', json=message_input).json()

    # Sleep the program for 2.1 seconds (0.1 extra as a buffer).
    sleep(2.1)

    # Get a list of all the messages that have been sent in the channel.
    function_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=function_input).json()
    assert message_from_data['messages'][0]['u_id'] == user['u_id']
    assert message_from_data['messages'][0]['message'] == 'Message'
    assert message_from_data['messages'][0]['message_id'] == message_info['message_id']


def test_sendlater_orderofmessageids(reset, new_user, new_channel):
    '''
    Testing the scenario where message_send is called between the time
    message_sendlater is called and when message_sendlater appends to
    the data_store.
    '''

    user = new_user()
    channel = new_channel(user)

    time_now = int(datetime.now(timezone.utc).timestamp())
    time_to_send = time_now + 2

    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message',
        'time_sent': time_to_send
    }

    message_info = requests.post(f'{BASE_URL}/message/sendlater', json=message_input).json()

    # Make a message_send request.
    message_send_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message'
    }

    message_send_info = requests.post(f'{BASE_URL}/message/send', json=message_send_input).json()

    # Sleep the program for 2.1 seconds (0.1 extra as a buffer).
    sleep(2.1)

    # Get a list of all the messages that have been sent in the channel.
    function_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=function_input).json()
    # While the message_send should append to the data_store first, thus having
    # the zero'th index, the earlier message_id should be on the message_sendlater
    # request, as it was sent earlier.
    assert message_from_data['messages'][0]['message_id'] == message_send_info['message_id']
    assert message_from_data['messages'][1]['message_id'] == message_info['message_id']

def test_sendlater_notadmin(reset, new_user, new_channel):
    '''
    Testing that a user that is not an admin will be able to use message
    sendlater.
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

    time_now = int(datetime.now(timezone.utc).timestamp())
    time_to_send = time_now + 2

    message_info = {
        'token': second_user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message',
        'time_sent': time_to_send
    }

    requests.post(f'{BASE_URL}/message/sendlater', json=message_info)

    # Sleep the program for 2.1 seconds (0.1 extra as a buffer).
    sleep(2.1)

    # Get a list of all the messages that have been sent in the channel.
    function_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_from_data = requests.get(f'{BASE_URL}/channel/messages', params=function_input).json()
    assert message_from_data['messages'][0]['u_id'] == second_user['u_id']


def test_sendlater_timeinpast(reset, new_user, new_channel):
    '''
    Testing that an error will be raised if the time_sent paramter is less
    than the time at the current moment.
    '''

    user = new_user()
    channel = new_channel(user)

    time_now = int(datetime.now(timezone.utc).timestamp())
    time_to_send = time_now - 2

    message_info = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Message',
        'time_sent': time_to_send
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/sendlater',
                      json=message_info).raise_for_status()



def test_sendlater_invalid_token(reset, new_user, new_channel):
    '''
    Testing that calling message_sendlater with an invalid token will
    raise an error.
    '''

    user = new_user()
    channel = new_channel(user)

    token = user['token']
    requests.post(f"{BASE_URL}/auth/logout", json={'token': token})

    time_now = int(datetime.now(timezone.utc).timestamp())
    time_to_send = time_now + 2

    message_info = {
        'token': token,
        'channel_id': channel['channel_id'],
        'message': 'Message',
        'time_sent': time_to_send
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/message/sendlater',
                      json=message_info).raise_for_status()
