import channels
import channel
import message
from error import AccessError
from error import InputError
import pytest
import auth

# =====================================================
# ========== TESTING MESSAGE REMOVE FUNCTION ==========
# =====================================================

def test_remove(test_channel, test_user):

    ''' Testing an average case where a user will remove their own message. '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_remove(test_user['token'], new_message['message_id'])


def test_remove_two(test_channel, test_user):

    ''' Case where a default user will remove multiple messages in a row. '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    second_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message2')

    message.message_remove(test_user['token'], second_message['message_id'])
    message.message_remove(test_user['token'], new_message['message_id'])


def test_remove_wrong_id(test_channel, test_user):

    ''' Testing if an InputError is thrown when an invalid message_id is input. '''

    with pytest.raises(InputError):
        message.message_remove(test_user['token'], 99999)


def test_remove_unauthorized(test_channel, test_user, new_user):

    ''' Testing that an AccessError is thrown when a default user is trying to remove
    another default user's message'''

    second_user = new_user('tester2@gmail.com')
    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])
    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(AccessError):
        message.message_remove(second_user['token'], new_message['message_id'])


def test_remove_owner(test_channel, test_user, new_user):

    ''' Testing that a channel owner has the ability to remove another user's message. '''

    second_user = new_user('tester3@gmail.com')
    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])

    new_message = message.message_send(second_user['token'], test_channel['channel_id'], 'Message')
    message.message_remove(test_user['token'], new_message['message_id'])


def test_remove_new_owners(test_channel, test_user, new_user):

    ''' Testing that added owners have the ability to remove other user's messages inside
    that channel '''

    second_user = new_user('test2@test.com')
    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])
    channel.channel_addowner(test_user['token'], test_channel['channel_id'], second_user['u_id'])

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')
    message.message_remove(second_user['token'], new_message['message_id'])


def test_remove_invalidtoken(test_channel, test_user):

    ''' Testing that an invalid token will raise an AccessError. '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'Message')

    with pytest.raises(AccessError):
        message.message_remove('NOTAVALIDTOKEN', new_message['message_id'])
