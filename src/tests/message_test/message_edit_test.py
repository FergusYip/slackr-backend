'''
System testing the functionality of message_edit.
'''

import pytest
import channel
import message
from error import AccessError
from error import InputError
import auth

# =====================================================
# ========== TESTING MESSAGE EDIT FUNCTION ============
# =====================================================

def test_edit_average(reset, test_channel, test_user): # pylint: disable=W0613
    '''
    Average case test where a user edits their own message.
    '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_edit(test_user['token'], new_message['message_id'], 'Message')


def test_edit_into_empty_string(reset, test_channel, test_user): # pylint: disable=W0613
    '''
    Testing the change from a string to an empty string. Should result in a deleted message.
    '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    message.message_edit(test_user['token'], new_message['message_id'], "")

    messages = channel.channel_messages(test_user['token'], test_channel['channel_id'], 0)

    assert not messages['messages']


def test_nomessage(reset, test_user, test_channel): # pylint: disable=W0613
    '''
    Testing that attempting to edit an invalid message will raise an error.
    '''

    with pytest.raises(InputError):
        message.message_edit(test_user['token'], 1, 'New Message')


def test_overcharacters(reset, test_user, test_channel): # pylint: disable=W0613
    '''
    Testing that attempting to edit a message to over 1,000 characters will
    raise an error.
    '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(InputError):
        message.message_edit(test_user['token'], new_message['message_id'], 'i' * 1001)


def test_edit_owner(reset, test_channel, test_user, new_user): # pylint: disable=W0613
    '''
    Testing the ability for the channel owner to edit a default user's message.
    '''

    second_user = new_user('tester2@gmail.com')
    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])

    new_message = message.message_send(second_user['token'], test_channel['channel_id'], 'Message')
    message.message_edit(test_user['token'], new_message['message_id'], 'New Message')


def test_edit_unauthorised(reset, test_channel, test_user, new_user): # pylint: disable=W0613
    '''
    Testing an AccessError thrown when a default user tries to edit an owner's message.
    '''

    second_user = new_user('tester2@gmail.com')
    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])
    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(AccessError):
        message.message_edit(second_user['token'], new_message['message_id'], 'New Message')


def test_edit_unauthorised_default(reset, test_channel, test_user, new_user): # pylint: disable=W0613
    '''
    Testing an AccessError thrown when a default user attempts to edit another
    default user's message.
    '''

    second_user = new_user('tester2@gmail.com')
    third_user = new_user('tester3@gmail.com')
    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])
    channel.channel_invite(test_user['token'], test_channel['channel_id'], third_user['u_id'])
    new_message = message.message_send(second_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(AccessError):
        message.message_edit(third_user['token'], new_message['message_id'], 'New Message')


def test_edit_invalidtoken(reset, test_channel, test_user): # pylint: disable=W0613
    '''
    Testing that an invalid token will raise an AccessError.
    '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    assert auth.auth_logout(test_user['token'])['is_success']

    with pytest.raises(AccessError):
        message.message_edit(test_user['token'], new_message['message_id'],
                             'New Message')
