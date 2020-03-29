'''
HTTP Tests for the standup_active function.
'''

from time import sleep
import requests
import pytest

BASE_URL = 'http://127.0.0.1:8080'


def test_invalid_channel(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing standup active for an invalid channel.
    '''

    user = new_user()
    new_channel(user)

    active_in = {
        'token': user['token'],
        'channel_id': -1
    }

    with pytest.raises(requests.HTTPError):
        requests.get(f'{BASE_URL}/standup/active',
                     params=active_in).raise_for_status()


def test_return(reset, new_user, new_channel):  # pylint: disable=W0613
    '''
    Testing return of standup active.
    '''

    user = new_user()
    channel = new_channel(user)

    start_in = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 1
    }

    # starting a standup.
    requests.post(f'{BASE_URL}/standup/start', json=start_in).json()

    active_in = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }

    active_out = requests.get(
        f'{BASE_URL}/standup/active', params=active_in).json()

    assert active_out['is_active']

    sleep(2)

    active_out = requests.get(
        f'{BASE_URL}/standup/active', params=active_in).json()

    assert active_out['is_active'] is False


def test_insufficient_params(reset):  # pylint: disable=W0613
    '''
    Testing insufficient parameters for standup active
    '''

    with pytest.raises(requests.HTTPError):
        requests.get(f"{BASE_URL}/standup/active",
                     params={}).raise_for_status()
