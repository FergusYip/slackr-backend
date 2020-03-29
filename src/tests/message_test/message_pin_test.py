'''
System testing the functionality of message_pin.
'''

import pytest
import channel
import message
import auth
from error import AccessError
from error import InputError

# =====================================================
# =========== TESTING MESSAGE PIN FUNCTION ============
# =====================================================

def test_pin(reset, test_channel, test_user):
    '''
    Testing the average case functionality of message_pin.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_pin(test_user['token'], message_info['message_id'])


def test_pin_invalid_message(reset, test_channel, test_user):
    '''
    Testing that attempting to pin an invalid message will raise an
    InputError.
    '''

    with pytest.raises(InputError):
        message.message_pin(test_user['token'], 1)

def test_pin_usernotadmin(reset, new_channel, new_user):
    '''
    Testing that attempting to pin a message whilst not being an admin
    or owner will raise an InputError.
    '''

    user = new_user()
    second_user = new_user(email='tester2@test.com')
    first_channel = new_channel(user)

    channel.channel_invite(user['token'], first_channel['channel_id'], second_user['u_id'])

    message_info = message.message_send(user['token'], first_channel['channel_id'], 'Message')

    with pytest.raises(InputError):
        message.message_pin(second_user['token'], message_info['message_id'])


def test_pin_messagealreadypinned(reset, test_channel, test_user):
    '''
    Testing that attempting to pin a message that is already pinned will
    raise an InputError.
    '''
    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_pin(test_user['token'], message_info['message_id'])

    with pytest.raises(InputError):
        message.message_pin(test_user['token'], message_info['message_id'])


def test_pin_usernotchannelmember(reset, test_channel, test_user):
    '''
    Testing that attempting to pin a message whilst not a channel member
    anymore will result in an AccessError.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    channel.channel_leave(test_user['token'], test_channel['channel_id'])

    with pytest.raises(AccessError):
        message.message_pin(test_user['token'], message_info['message_id'])

def test_pin_invalid_token(reset, test_channel, test_user):
    '''
    Testing that attempting to pin a message whilst having an invalid
    token will raise an AccessError.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    assert auth.auth_logout(test_user['token'])['is_success']

    with pytest.raises(AccessError):
        message.message_pin(test_user['token'], message_info['message_id'])
