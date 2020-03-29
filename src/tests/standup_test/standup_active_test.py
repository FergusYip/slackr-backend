'''
System testing the standup_active function.
'''

import pytest
from error import InputError, AccessError
from datetime import datetime, timezone
import standup
import channel
from time import sleep

NoneType = type(None)

# =====================================================
# ========= TESTING STANDUP ACTIVE FUNCTION ===========
# =====================================================

def test_active_return(reset, test_channel, test_user):
    '''
    Testing the return values of standup_active.
    '''

    standup.standup_start(test_user['token'], test_channel['channel_id'], 1)
    standup_return = standup.standup_active(test_user['token'], test_channel['channel_id'])
    
    assert isinstance(standup_return, dict)
    assert isinstance(standup_return['is_active'], bool)
    assert isinstance(standup_return['time_finish'], int)

    sleep(1.1)

    standup_return = standup.standup_active(test_user['token'], test_channel['channel_id'])
    
    assert isinstance(standup_return, dict)
    assert isinstance(standup_return['is_active'], bool)
    assert isinstance(standup_return['time_finish'], NoneType)

def test_active_true(reset, test_channel, test_user):
    '''
    Testing the first average case functionality of standup_active.
    '''

    standup.standup_start(test_user['token'], test_channel['channel_id'], 1)

    time_to_finish = int(datetime.now(timezone.utc).timestamp()) + 1

    standup_return = standup.standup_active(test_user['token'], test_channel['channel_id'])
    assert standup_return['time_finish'] == time_to_finish
    assert standup_return['is_active']

    sleep(1.1)

    standup_return = standup.standup_active(test_user['token'], test_channel['channel_id'])
    assert not standup_return['is_active']
    assert not standup_return['time_finish']


def test_active_false(reset, test_channel, test_user):
    '''
    Testing the second average case functionality of standup_active. Where
    a user calls standup_active before any have started.
    '''

    standup_return = standup.standup_active(test_user['token'], test_channel['channel_id'])
    assert not standup_return['is_active']


def test_active_insufficientparams(reset, test_channel, test_user):
    '''
    Testing that inputting None into the function will raise an InputError.
    '''

    with pytest.raises(InputError):
        standup.standup_active(test_user['token'], None)


def test_active_invalidchannel(reset, test_user):
    '''
    Testing that calling standup_active in an invalid channel will
    raise an InputError.
    '''

    with pytest.raises(InputError):
        standup.standup_active(test_user['token'], 1)


def test_active_invalidtoken(reset, test_channel, invalid_token):
    '''
    Testing that calling standup_active will raise an error if
    an invalid token is input.
    '''

    with pytest.raises(AccessError):
        standup.standup_active(invalid_token, test_channel['channel_id'])
