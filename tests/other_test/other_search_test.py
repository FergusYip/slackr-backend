'''Pytest script for testing search route'''

import requests
import pytest
from error import AccessError

BASE_URL = 'http://127.0.0.1:8080'


def test_search_return_type(reset, new_user, new_channel):
    '''Test the types of values returned by search'''
    user = new_user()
    channel = new_channel(target_user='user')

    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello world!'
    }
    requests.post(f'{BASE_URL}/message/send', json=message_input)

    search_input = {'token': user['token'], 'query_str': 'Hello'}
    search = requests.get(f'{BASE_URL}/search', json=search_input).json()

    assert isinstance(search, dict)
    assert isinstance(search['message_id'], int)
    assert isinstance(search['u_id'], int)
    assert isinstance(search['message'], str)
    assert isinstance(search['time_created'], int)


def test_search_no_channel(reset, new_user):
    '''Test search function when there is no channel'''

    user = new_user()
    search_input = {'token': user['token'], 'query_str': ''}
    search = requests.get(f'{BASE_URL}/search', json=search_input).json()

    assert len(search['messages']) == 0


def test_search_empty_channel(reset, new_user, new_channel):
    '''Test search function when channel has no messages'''

    user = new_user()
    new_channel(target_user='user')

    search_input = {'token': user['token'], 'query_str': ''}
    search = requests.get(f'{BASE_URL}/search', json=search_input).json()

    assert len(search['messages']) == 0


def test_search_single_channel(reset, new_user, new_channel):
    '''Test that the sole message is returned by search'''

    user = new_user()
    channel = new_channel(user)

    message_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'Hello world!'
    }
    requests.post(f'{BASE_URL}/message/send', json=message_input)

    search_input = {'token': user['token'], 'query_str': 'Hello'}
    search = requests.get(f'{BASE_URL}/search', json=search_input).json()

    message_from_search = search['messages'][0]

    messages_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    channel_messages = requests.get(f'{BASE_URL}/channel/messages',
                                    json=messages_input).json()

    message_from_channel = channel_messages['messages'][0]

    assert message_from_search == message_from_channel


def test_search_multiple_messages(reset, new_user, new_channel, send_msg):
    '''Test search with multiple unique messages'''

    user = new_user()
    channel = new_channel(user)

    send_msg(user['token'], channel['channel_id'], 'Alpha')
    send_msg(user['token'], channel['channel_id'], 'Bravo')
    send_msg(user['token'], channel['channel_id'], 'Charlie')

    search_input_a = {'token': user['token'], 'query_str': 'a'}
    search_input_b = {'token': user['token'], 'query_str': 'b'}
    search_input_romeo = {'token': user['token'], 'query_str': 'Romeo'}

    search_a = requests.get(f'{BASE_URL}/search', json=search_input_a).json()
    search_b = requests.get(f'{BASE_URL}/search', json=search_input_b).json()
    search_romeo = requests.get(f'{BASE_URL}/search',
                                json=search_input_romeo).json()

    assert len(search_a['messages']) == 3
    assert len(search_b['messages']) == 1
    assert len(search_romeo['messages']) == 0


def test_search_multiple_channels(reset, new_user, new_channel, send_msg):
    '''Test that search works on multiple channels'''

    user = new_user()

    ch1 = new_channel(user, 'Channel 1')
    send_msg(user['token'], ch1['channel_id'], 'Channel 1')

    ch2 = new_channel(user, 'Channel 2')
    send_msg(user['token'], ch2['channel_id'], 'Channel 2')

    ch3 = new_channel(user, 'Channel 3')
    send_msg(user['token'], ch3['channel_id'], 'Channel 3')

    search_input = {'token': user['token'], 'query_str': 'Channel'}
    search = requests.get(f'{BASE_URL}/search', json=search_input).json()

    assert len(search['messages']) == 3


def test_search_unauthorised_channels(reset, new_user, new_channel, send_msg):
    '''Test that users cannot search unauthorised channels'''

    tom = new_user(email='tom@email.com')

    jerry = new_user(email='jerry@email.com')

    mice_channel = new_channel(jerry, 'Mice Only')

    send_msg(jerry['token'], mice_channel['channel_id'], 'Tom can\'t see this')

    search_input_tom = {'token': tom['token'], 'query_str': ''}
    search_input_jerry = {'token': jerry['token'], 'query_str': ''}

    search_tom = requests.get(f'{BASE_URL}/search',
                              json=search_input_tom).json()

    search_jerry = requests.get(f'{BASE_URL}/search',
                                json=search_input_jerry).json()

    assert len(search_jerry['messages']) == 1
    assert len(search_tom['messages']) == 0


def test_search_case_insensitive(reset, new_user, new_channel, send_msg):
    '''Test that query string is not case sensitive'''

    user = new_user()
    channel = new_channel(user, 'Channel')

    send_msg(user['token'], channel['channel_id'], 'Hello world!')

    messages_input = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }
    channel_messages = requests.get(f'{BASE_URL}/channel/messages',
                                    json=messages_input).json()
    message_from_channel = channel_messages['messages'][0]

    search_input = {'token': user['token'], 'query_str': 'hello'}
    search = requests.get(f'{BASE_URL}/search', json=search_input).json()
    message_from_search = search['messages'][0]

    assert message_from_search == message_from_channel


def test_search_invalid_token(reset, invalid_token):
    '''Test search function with invalid token'''

    search_input = {'token': invalid_token, 'query_str': ''}

    with pytest.raises(AccessError):
        requests.get(f'{BASE_URL}/search', json=search_input).json()
