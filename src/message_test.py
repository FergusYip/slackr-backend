# Testing the message.py file

import channels
import channel
import message
from error import AccessError
from error import InputError
import pytest
import auth

# ========== TESTING MESSAGE SEND FUNCTION ==========

# Simple tests of average case messages.
def test_message_send():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')

    channel_id = channels.create(new_user['token'], 'Channel1', True)

    new_message = message.send(new_user['token'], channel_id['channel_id'], 'Hello world!')
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0)

    assert(new_message['message_id'] == messages[0]['message_id'])

    second_message = message.send(new_user['token'], channel_id['channel_id'], 'testingamessagenospaces')
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0)

    assert(second_message['message_id'] == messages[0]['message_id'])

    third_message = message.send(new_user['token'], channel_id['channel_id'], 'test message 123')
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0)

    assert(second_message['message_id'] == messages[1]['message_id'])

# Testing unauthorized sending of messages.
def test_unauthorized():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')

    channel_id = channels.create(new_user['token'], 'Channel2', False)

    with pytest.raises(AccessError) as e:
        message.send(new_user['token'], channel_id['channel_id'], 'Hello team')

# Testing a change in authorization affecting message sending.
def test_authorization_change():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')

    channel_id = channels.create(new_user['token'], 'Channel3', False)

    second_user = auth.register('letmein@test.com', 'Password1', 'Sample', 'Name')

    with pytest.raises(AccessError) as e:
        message.send(second_user['token'], channel_id['channel_id'], 'Why wont this send?')

    channel.invite(new_user['token'], channel_id['channel_id'], second_user['u_id'])

    new_message = message.send(second_user['token'], channel_id['channel_id'], 'Hello World!')
    messages = channel.messages(second_user['token'], channel_id['channel_id'], 0)

    assert(new_message['message_id'] == messages[0]['message_id'])

# Testing an incorrect character length string message.
def test_inputErrors():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')

    channel_id = channels.create(new_user['token'], 'Channel4', True)

    with pytest.raises(InputError) as e:
        message.send(new_user['token'], channel_id['channel_id'], 'i' * 1001)

    new_message = message.send(second_user['token'], channel_id['channel_id'], 'i' * 1000)
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0)

    assert(new_message['message_id'] == messages[0]['message_id'])

# ========== TESTING MESSAGE REMOVE FUNCTION ==========

def test_messageInputError():
    pass



# ========== TESTING MESSAGE EDIT FUNCTION ==========
