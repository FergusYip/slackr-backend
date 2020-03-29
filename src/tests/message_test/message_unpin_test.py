'''
System testing the functionality of message_unpin.
'''

import pytest
import channel
import message
import auth
from error import AccessError
from error import InputError

# =====================================================
# ========== TESTING MESSAGE UNPIN FUNCTION ===========
# =====================================================

def test_unpin(reset, test_channel, test_user):
    '''
    Testing the average case functionality of message_pin.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_pin(test_user['token'], message_info['message_id'])

    message.message_unpin(test_user['token'], message_info['message_id'])


def test_unpin_invalid_message(reset, test_user):
    '''
    Testing that attempting to unpin an invalid message will raise an
    InputError.
    '''

    with pytest.raises(InputError):
        message.message_unpin(test_user['token'], 1)

def test_unpin_notadmin(reset, new_channel, new_user):
    '''
    Testing that if a user other than an admin attempts to unpin a message,
    an InputError will be raised.
    '''

    first_user = new_user()
    second_user = new_user(email='tester2@test.com')

    first_channel = new_channel(first_user)

    channel.channel_invite(first_user['token'], first_channel['channel_id'], second_user['u_id'])

    message_info = message.message_send(first_user['token'], first_channel['channel_id'], 'Message')
    message.message_pin(first_user['token'], message_info['message_id'])

    with pytest.raises(InputError):
        message.message_unpin(second_user['token'], message_info['message_id'])


def test_unpin_notpinned(reset, test_channel, test_user):
    '''
    Testing that attempting to unpin a message that is not pinned
    will raise an InputError.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(InputError):
        message.message_unpin(test_user['token'], message_info['message_id'])


def test_unpin_notchannelmember(reset, test_channel, test_user):
    '''
    Testing that if an admin is no longer in the channel, an InputError will be
    raised if they attempt to unpin a message.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_pin(test_user['token'], message_info['message_id'])

    channel.channel_leave(test_user['token'], test_channel['channel_id'])

    with pytest.raises(AccessError):
        message.message_unpin(test_user['token'], message_info['message_id'])


def test_unpin_invalid_token(reset, test_channel, test_user):
    '''
    Testing that attempting to unpin a message with an invalid token will
    raise an AccessError.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_pin(test_user['token'], message_info['message_id'])

    assert auth.auth_logout(test_user['token'])['is_success']

    with pytest.raises(AccessError):
        message.message_unpin(test_user['token'], message_info['message_id'])