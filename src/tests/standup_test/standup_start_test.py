'''
System testing the standup_start function.
'''

from time import sleep
import pytest
from error import InputError, AccessError
import standup
import channel

# =====================================================
# ========= TESTING STANDUP START FUNCTION ============
# =====================================================

def test_standup_start(reset, test_channel, test_user):
    '''
    Testing the average case use of standup_start in a channel. Must ensure
    the standup starts and stops eventually. At completition, it should send
    all messsages that have been sent as a singular message in the channel.
    '''

    standup.standup_start(test_user['token'], test_channel['channel_id'], 1)
    standup.standup_send(test_user['token'], test_channel['channel_id'], 'Message')

    sleep(1.1)

    message_list = channel.channel_messages(test_user['token'], test_channel['channel_id'], 0)

    # Assert that there is a message in the zero'th index position.
    assert message_list['messages'][0]['message']

def test_standup_insufficientparams(reset, test_user):
    '''
    Testing that giving the standup_start function insufficient parameters
    will raise an InputError.
    '''

    with pytest.raises(InputError):
        standup.standup_start(test_user['token'], None, 1)

def test_standup_channelnotexist(reset, test_user):
    '''
    Testing that attempting to start a standup in a channel that does not
    exist will raise an InputError.
    '''

    with pytest.raises(InputError):
        standup.standup_start(test_user['token'], 1, 1)


def test_standup_standupalreadyactive(reset, test_channel, test_user):
    '''
    Testing that attempting to start a standup whilst one is already active
    will result in an InputError.
    '''

    standup.standup_start(test_user['token'], test_channel['channel_id'], 1)

    with pytest.raises(InputError):
        standup.standup_start(test_user['token'], test_channel['channel_id'], 1)


def test_standup_invalid_token(reset, test_channel, invalid_token):
    '''
    Testing that attempting to start a standup with an invalid token will raise an
    AccessError.
    '''

    with pytest.raises(AccessError):
        standup.standup_start(invalid_token, test_channel['channel_id'], 1)
