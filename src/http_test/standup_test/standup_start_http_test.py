'''
HTTP Tests for the standup_start function.
'''

from datetime import datetime, timezone
from time import sleep
import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_standup_start(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing the standup start function.
    '''

    user = new_user()
    channel = new_channel(user)

    start_in = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 1
    }

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


def test_invalid_channel(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing the standup start function for an invalid channel id.
    '''

    user = new_user()
    new_channel(user)

    start_in = {
        'token': user['token'],
        'channel_id': -1,
        'length': 1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/standup/start',
                      json=start_in).raise_for_status()


def test_start_return(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing the time_finish returned by standup_start.
    '''

    user1 = new_user()

    channel = new_channel(user1)

    start_in = {
        'token': user1['token'],
        'channel_id': channel['channel_id'],
        'length': 1
    }

    finish_exp = int(datetime.now(timezone.utc).timestamp()) + \
        start_in['length']
    finish = requests.post(f'{BASE_URL}/standup/start', json=start_in).json()

    sleep(1.1)

    assert finish_exp == finish['time_finish']


def test_invalid_id(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing standup start for an invalid channel id.
    '''

    user1 = new_user()

    new_channel(user1)

    start_in = {
        'token': user1['token'],
        'channel_id': -1,
        'length': 1
    }

    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/standup/start',
                      json=start_in).raise_for_status()


def test_active_standup(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing standup start when an active standup is already running.
    '''

    user = new_user()
    channel = new_channel(user)

    start_in = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 1
    }

    requests.post(f'{BASE_URL}/standup/start', json=start_in)

    # should raise an error when a standup is already active.
    with pytest.raises(requests.HTTPError):
        requests.post(f'{BASE_URL}/standup/start',
                      json=start_in).raise_for_status()


def test_insufficient_params(reset):
    '''
    Testing insufficient parameters for standup start
    '''

    with pytest.raises(requests.HTTPError):
        requests.post(f"{BASE_URL}/standup/start",
                      json={}).raise_for_status()
