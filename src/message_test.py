# Testing the message.py file

import channels
import channel
import message
from error import AccessError
import pytest
import auth

# ========== TESTING MESSAGE SEND FUNCTION ==========

# Simple tests of average case messages.
def test_message_send():
    auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    assert(channels.create('12345', 'Hello', True)
    == {'channel_id' : 1})
    assert(message.send('12345', 1, 'Hello world!')
    == {'message_id' : 1})
    assert(message.send('12345', 1, 'testingamessagenospaces')
    == {'message_id' : 1})
    assert(message.send('12345', 1, '12176182812')
    == {'message_id' : 1})

# Testing unauthorized sending of messages.
def test_unauthorized():
    auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    assert(channels.create('12345', 'areyouallowedin', False)
    == {'channel_id' : 1})
    with pytest.raises(AccessError) as e:
        message.send('12345', 1, 'Hello team')

# Testing a change in authorization affecting message sending.
def test_authorization_change():
    auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    assert(channels.create('12345', 'WorkChannelTest', False)
    == {'channel_id' : 1})
    with pytest.raises(AccessError) as f:
        message.send('12345', 1, 'Text Example')
    channel.invite('12345', 1, 1)
    assert(message.send('12345', 1, 'Hello World!') == { 'message_id' : 1})

# Testing an incorrect character length string message.
def test_inputErrors():
    auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    assert(channels.create('12345', 'NewChannel', True))
    with pytest.raises(InputError) as g:
        message.send('12345', 1, 'i' * 1001)
    assert(message.send('12345', 1, 'Hello World!') == {'message_id' : 1})

# ========== TESTING MESSAGE REMOVE FUNCTION ==========

# ========== TESTING MESSAGE EDIT FUNCTION ==========
