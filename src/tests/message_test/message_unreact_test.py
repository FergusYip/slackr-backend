'''
System testing the message_unreact functionality.
'''

import pytest
import channel
import message
import auth
from error import AccessError
from error import InputError

# =====================================================
# ========= TESTING MESSAGE UNREACT FUNCTION ==========
# =====================================================

def test_unreact_single(reset, test_channel, test_user):
    '''
    Testing one average case where a user will remove the only reaction from
    the message.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_react(test_user['token'], message_info['message_id'], 1)

    message.message_unreact(test_user['token'], message_info['message_id'], 1)

def test_unreact_multiple(reset, new_channel, new_user):
    '''
    Testing the other average case where a user will remove their
    reaction whilst other u_ids have also reacted.
    '''

    first_user = new_user()
    second_user = new_user(email='tester2@test.com')

    first_channel = new_channel(first_user)
    channel.channel_invite(first_user['token'], first_channel['channel_id'], second_user['u_id'])

    message_info = message.message_send(first_user['token'], first_channel['channel_id'], 'Message')

    message.message_react(first_user['token'], message_info['message_id'], 1)
    message.message_react(second_user['token'], message_info['message_id'], 1)

    message.message_unreact(second_user['token'], message_info['message_id'], 1)


def test_unreact_invalid_message(reset, test_channel, test_user):
    '''
    Testing that attempting to unreact to an invalid message will result
    in an InputError being raised.
    '''

    with pytest.raises(InputError):
        message.message_unreact(test_user['token'], 1, 1)


def test_unreact_notinchannel(reset, test_channel, test_user):
    '''
    Testing that attempting to unreact to a message while the user is not in
    the channel will result in an InputError being raised.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_react(test_user['token'], message_info['message_id'], 1)

    channel.channel_leave(test_user['token'], test_channel['channel_id'])

    with pytest.raises(InputError):
        message.message_unreact(test_user['token'], message_info['message_id'], 1)


def test_unreact_invalid_reactid(reset, test_channel, test_user):
    '''
    Testing that attempting to unreact with an invalid react_id will raise
    an InputError.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_react(test_user['token'], message_info['message_id'], 1)

    with pytest.raises(InputError):
        message.message_unreact(test_user['token'], message_info['message_id'], 2)


def test_unreact_notyetreacted(reset, test_channel, test_user):
    '''
    Testing that attempting to remove a react when the user has not yet reacted
    will result in an InputError.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(InputError):
        message.message_unreact(test_user['token'], message_info['message_id'], 1)


def test_unreact_uidnotreacted(reset, new_channel, new_user):
    '''
    Testing that attempting to remove a react when the user has not yet reacted,
    yet other u_ids have reacted will result in an InputError.
    '''

    first_user = new_user()
    second_user = new_user(email='tester2@test.com')

    first_channel = new_channel(first_user)
    channel.channel_invite(first_user['token'], first_channel['channel_id'], second_user['u_id'])

    message_info = message.message_send(first_user['token'], first_channel['channel_id'], 'Message')

    message.message_react(first_user['token'], message_info['message_id'], 1)

    with pytest.raises(InputError):
        message.message_unreact(second_user['token'], message_info['message_id'], 1)


def test_unreact_invalid_token(reset, test_channel, test_user):
    '''
    Testing that attempting to unreact to a message with an invalid
    token will raise an AccessError.
    '''

    message_info = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_react(test_user['token'], message_info['message_id'], 1)

    assert auth.auth_logout(test_user['token'])['is_success']

    with pytest.raises(AccessError):
        message.message_unreact(test_user['token'], message_info['message_id'], 1)