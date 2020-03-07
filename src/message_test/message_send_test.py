import channels
import channel
import message
from error import AccessError
from error import InputError
import pytest
import auth

# =====================================================
# ========== TESTING MESSAGE SEND FUNCTION ============
# =====================================================

def test_send(test_channel, test_user):

    ''' Testing an average case where a created user in a channel sends a message '''

    message.message_send(test_user['token'], test_channel['channel_id'], 'Message')


def test_send_unauthorized(test_channel, test_user, new_user):

    ''' Testing that an AccessError is thrown when a user attempts to send a
    message in a channel to which they are not joined. '''

    second_user = new_user('test@test.com')

    with pytest.raises(AccessError):
        message.message_send(second_user['token'], test_channel['channel_id'], 'Message')


def test_send_authorization_change(test_channel, test_user, new_user):

    ''' Testing a scenario where a user attempts to send a message in a server they have
    not joined. This should throw an AccessError. After a channel invitation they should
    be able to send messages inside the channel. '''

    second_user = new_user('tester2@test.com')

    with pytest.raises(AccessError):
        message.message_send(second_user['token'], test_channel['channel_id'], 'Message')

    channel.channel_invite(test_user['token'], test_channel['channel_id'], second_user['u_id'])

    message.message_send(second_user['token'], test_channel['channel_id'], 'Message')


def test_send_exceed_char_limit(test_channel, test_user):

    ''' Testing an InputError that should be thrown when the message is greater than
    1000 characters. '''

    with pytest.raises(InputError):
        message.message_send(test_user['token'], test_channel['channel_id'], 'i' * 1001)


def test_send_within_char_limit(test_channel, test_user):

    ''' Testing the maximum length of a message sends correctly. '''

    new_message = message.message_send(test_user['token'], test_channel['channel_id'], 'i' * 1000)


def test_send_empty(test_channel, test_user, new_user):

    ''' Testing that a message of zero characters raises an InputError. '''

    with pytest.raises(InputError):
        message.message_send(test_user['token'], test_channel['channel_id'], '')


def test_send_invalidtoken(test_channel, test_user, invalid_token):

    ''' Testing that an invalid token will raise an AccessError. '''

    with pytest.raises(AccessError):
        message.message_send(invalid_token, test_channel['channel_id'],
                             'Message')
