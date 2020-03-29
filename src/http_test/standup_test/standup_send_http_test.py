'''
HTTP Tests for the standup_send function.
'''

from time import sleep
import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_invalid_channel(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing standup send for an invalid channel id.
    '''

    user = new_user()
    channel = new_channel(user)

    start_in = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 1
    }

    # starting standup
    requests.post(f'{BASE_URL}/standup/start', json=start_in).json()

    send_in = {
        'token': user['token'],
        'channel_id': -1,
        'message': 'hello'
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/standup/send',
                      json=send_in).raise_for_status()


def test_standup_send(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing the standup send function.
    '''

    user = new_user()
    channel = new_channel(user)

    start_in = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 1
    }

    # starting standup.
    requests.post(f'{BASE_URL}/standup/start', json=start_in).json()

    message_in = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'hello'
    }

    requests.post(f'{BASE_URL}/standup/send', json=message_in)

    history_in = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'start': 0
    }

    message_hist = requests.get(
        f'{BASE_URL}/channel/messages', params=history_in).json()

    # should be empty before 1s has passed.
    assert not message_hist['messages']

    sleep(1.1)

    message_hist = requests.get(
        f'{BASE_URL}/channel/messages', params=history_in).json()

    assert len(message_hist['messages']) == 1


def test_too_long(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing standup send when message is over 1000 characters long.
    '''

    user = new_user()
    channel = new_channel(user)

    start_in = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 1
    }

    # starting standup.
    requests.post(f'{BASE_URL}/standup/start', json=start_in).json()

    send_in = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'i'*1001
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/standup/send',
                      json=send_in).raise_for_status()


def test_inactive(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing standup send when a standup is not active.
    '''

    user = new_user()
    channel = new_channel(user)

    send_in = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': 'hello'
    }

    # standup has not been started.
    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/standup/send',
                      json=send_in).raise_for_status()


def test_non_member(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing standup send when the user is not a member of channel.
    '''

    user = new_user()
    user2 = new_user(email='user2@google.com')
    channel = new_channel(user)

    start_in = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 1
    }

    # starting standup.
    requests.post(f'{BASE_URL}/standup/start', json=start_in).json()

    send_in = {
        'token': user2['token'],
        'channel_id': channel['channel_id'],
        'message': 'hello'
    }

    # user2 is not member of the channel.
    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/standup/send',
                      json=send_in).raise_for_status()
