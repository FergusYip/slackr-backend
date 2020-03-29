'''
System testing the functionality of message_remove.
'''

import pytest
import channel
import message
from error import AccessError
from error import InputError
import auth

# =====================================================
# ========== TESTING MESSAGE REMOVE FUNCTION ==========
# =====================================================

def test_remove(reset, test_channel, test_user): # pylint: disable=W0613
    '''
    Testing an average case where a user will remove their own message.
    '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_remove(test_user['token'], new_message['message_id'])


def test_remove_two(reset, test_channel, test_user): # pylint: disable=W0613
    '''
    Case where a default user will remove multiple messages in a row.
    '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    second_message = message.message_send(test_user['token'],
                                          test_channel['channel_id'], 'Message2')

    message.message_remove(test_user['token'], second_message['message_id'])
    message.message_remove(test_user['token'], new_message['message_id'])


def test_remove_wrong_id(reset, test_channel, test_user): # pylint: disable=W0613
    '''
    Testing if an InputError is thrown when an invalid message_id is input.
    '''

    with pytest.raises(InputError):
        message.message_remove(test_user['token'], -1)


def test_remove_unauthorized(reset, test_channel, test_user, new_user): # pylint: disable=W0613
    '''
    Testing that an AccessError is thrown when a default user is trying to remove
    another default user's message
    '''

    second_user = new_user('tester2@gmail.com')
    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])
    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(AccessError):
        message.message_remove(second_user['token'], new_message['message_id'])


def test_remove_owner(reset, test_channel, test_user, new_user): # pylint: disable=W0613
    '''
    Testing that a channel owner has the ability to remove another user's message.
    '''

    second_user = new_user('tester3@gmail.com')
    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])

    new_message = message.message_send(second_user['token'], test_channel['channel_id'], 'Message')
    message.message_remove(test_user['token'], new_message['message_id'])


def test_remove_invalidtoken(reset, test_channel, test_user): # pylint: disable=W0613
    '''
    Testing that an invalid token will raise an AccessError.
    '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    assert auth.auth_logout(test_user['token'])['is_success']

    with pytest.raises(AccessError):
        message.message_remove(test_user['token'], new_message['message_id'])
