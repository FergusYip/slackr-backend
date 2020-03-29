import pytest
from error import InputError, AccessError
from datetime import datetime, timezone
import standup
import auth
import channel
from time import sleep

# =====================================================
# ========== TESTING STANDUP SEND FUNCTION ============
# =====================================================

def test_standupsend_return(reset, test_channel, test_user):
    '''
    Testing the return type of the standup_send function.
    '''

    standup.standup_start(test_user['token'], test_channel['channel_id'], 1)

    standup_return = standup.standup_send(test_user['token'], test_channel['channel_id'], 'Message')
    assert isinstance(standup_return, dict)
    assert not standup_return


def test_standupsend(reset, test_channel, test_user):
    '''
    Testing the average case functionality of the standup_send function.
    '''

    standup.standup_start(test_user['token'], test_channel['channel_id'], 1)

    standup_return = standup.standup_active(test_user['token'], test_channel['channel_id'])
    assert standup_return['is_active']

    standup.standup_send(test_user['token'], test_channel['channel_id'], 'Message')

    sleep(1.1)

    message_list = channel.channel_messages(test_user['token'], test_channel['channel_id'], 0)
    
    # Assert that there is a message in the zero'th index position.
    assert message_list['messages'][0]['message']


def test_standupsend_insufficientparams(reset, test_channel, test_user):
    '''
    Testing that if None is passed into the function, an InputError
    will be raised.
    '''

    standup.standup_start(test_user['token'], test_channel['channel_id'], 1)

    with pytest.raises(InputError):
        standup.standup_send(test_user['token'], test_channel['channel_id'], None)


def test_standupsend_invalidchannel(reset, test_user):
    '''
    Testing that attempting to send a message in standup mode
    in an invalid channel will raise an error.
    '''
    
    with pytest.raises(InputError):
        standup.standup_send(test_user['token'], 1, 'Message')


def test_standupsend_toolong(reset, test_channel, test_user):
    '''
    Testing that attempting to send a message greater than 1,000 characters
    will raise an error.
    '''

    standup.standup_start(test_user['token'], test_channel['channel_id'], 1)

    with pytest.raises(InputError):
        standup.standup_send(test_user['token'], test_channel['channel_id'], 'i' * 1001)


def test_standupsend_tooshort(reset, test_channel, test_user):
    '''
    Testing that attempting to send a standup_send that has a message
    that is zero characters will raise an error.
    '''

    standup.standup_start(test_user['token'], test_channel['channel_id'], 1)

    with pytest.raises(InputError):
        standup.standup_send(test_user['token'], test_channel['channel_id'], '')


def test_standupsend_falseactive(reset, test_channel, test_user):
    '''
    Testing that attempting to send a standup_send while no standup
    is running will raise an error.
    '''

    with pytest.raises(InputError):
        standup.standup_send(test_user['token'], test_channel['channel_id'], 'Message')


def test_standupsend_usernotinchannel(reset, test_channel, test_user, new_user):
    '''
    Testing that an error should be raised if the user is not in the channel
    that standup is running in.
    '''

    first_user = new_user()

    standup.standup_start(test_user['token'], test_channel['channel_id'], 1)

    with pytest.raises(AccessError):
        standup.standup_send(first_user['token'], test_channel['channel_id'], 'Message')


def test_standupsend_invalid_token(reset, new_channel, new_user):
    '''
    Testing that calling standup_send will raise an error if
    an invalid token is input.
    '''

    first_user = new_user()
    first_channel = new_channel(first_user)

    standup.standup_start(first_user['token'], first_channel['channel_id'], 1)

    assert auth.auth_logout(first_user['token'])['is_success']

    with pytest.raises(AccessError):
        standup.standup_send(first_user['token'], first_channel['channel_id'], 'Message')
