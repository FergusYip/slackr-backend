'''
System testing the functionality of message_react.
'''

import pytest
import message
import auth
from error import AccessError
from error import InputError

# =====================================================
# ========== TESTING MESSAGE REACT FUNCTION ===========
# =====================================================

def test_react(reset, test_channel, test_user):
    '''
    Testing the average case scenario where a user reacts to a message.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    message.message_react(test_user['token'], message_info['message_id'], 1)

def test_react_invalid_message(reset, test_user):
    '''
    Testing that attempting to react to an invalid message will raise an
    InputError.
    '''

    with pytest.raises(InputError):
        message.message_react(test_user['token'], 1, 1)

def test_react_notinchannel(reset, new_channel, test_user, new_user):
    '''
    Testing that attempting to react to a message inside a channel
    the user is not a part of, will raise an InputError.
    '''

    user = new_user()
    first_channel = new_channel(user)

    message_info = message.message_send(user['token'], first_channel['channel_id'], 'Message')

    with pytest.raises(InputError):
        message.message_react(test_user['token'], message_info['message_id'], 1)

def test_react_invalid_reactid(reset, test_channel, test_user):
    '''
    Testing that attempting to a message with an invalid react_id will raise
    an InputError.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(InputError):
        message.message_react(test_user['token'], message_info['message_id'], 2)


def test_react_already_reacted(reset, test_channel, test_user):
    '''
    Testing that attempting to react to a message the user has already reacted
    to will raise an InputError.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    message.message_react(test_user['token'], message_info['message_id'], 1)

    with pytest.raises(InputError):
        message.message_react(test_user['token'], message_info['message_id'], 1)


def test_react_invalid_token(reset, test_channel, test_user):
    '''
    Testing that an invalid token will raise an AccessError.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    assert auth.auth_logout(test_user['token'])['is_success']

    with pytest.raises(AccessError):
        message.message_react(test_user['token'], message_info['message_id'], 1)
