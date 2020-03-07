import channels
import channel
import message
from error import AccessError
from error import InputError
import pytest
import auth

# =====================================================
# ========== TESTING MESSAGE EDIT FUNCTION ============
# =====================================================

def test_edit_average(test_channel, test_user):

    ''' Average case test where a user edits their own message. '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_edit(test_user['token'], new_message['message_id'], 'Message')


def test_edit_into_empty_string(test_channel, test_user):

    ''' Testing the change from a string to an empty string. Should result in a deleted message. '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_edit(test_user['token'], new_message['message_id'], "")
    messages = channel.channel_messages(test_user['token'], test_channel['channel_id'], 0)

    assert(new_message['message_id'] != messages['messages'][0]['message_id'])


def test_edit_owner(test_channel, test_user, new_user):

    ''' Testing the ability for the channel owner to edit a default user's message. '''

    second_user = new_user('tester2@gmail.com')
    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])

    new_message = message.message_send(second_user['token'], test_channel['channel_id'], 'Message')
    message.message_edit(test_user['token'], new_message['message_id'], 'New Message')


def test_edit_unauthorised(test_channel, test_user, new_user):

    ''' Testing an AccessError thrown when a default user tries to edit an owner's message. '''

    second_user = new_user('tester2@gmail.com')
    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])
    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(AccessError):
        message.message_edit(second_user['token'], new_message['message_id'], 'New Message')


def test_edit_unauthorised_default(test_channel, test_user, new_user):

    ''' Testing an AccessError thrown when a default user attempts to edit another default user's message. '''

    second_user = new_user('tester2@gmail.com')
    third_user = new_user('tester3@gmail.com')
    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])
    channel.channel_invite(test_user['token'], test_channel['channel_id'], third_user['u_id'])
    new_message = message.message_send(second_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(AccessError):
        message.message_edit(third_user['token'], new_message['message_id'], 'New Message')


def test_edit_invalidtoken(test_channel, test_user, invalid_token):

    ''' Testing that an invalid token will raise an AccessError. '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(AccessError):
        message.message_edit(invalid_token, new_message['message_id'],
                             'New Message')
