# Testing the message.py file

import channels
import channel
import message
from error import AccessError
import pytest
import user
import auth

# Simple tests of average case messages.
def test_message_send():
    channels.create('12345', 'Hello')
    assert(message.send('12345', 6, 'Hello world!') == {'message_id' : 1})
    assert(message.send('22342', 1, 'testingamessagenospaces') == {'message_id' : 1})
    assert(message.send('32982', 37, '12176182812') == {'message_id' : 1})

def test_unauthorized():
    assert(channels.create('12345', 'areyouallowedin', False) == {'channel_id' : 1})
    with pytest.raises(AccessError) as e:
        assert(message.send('12345', 1, 'Hello team'))
    with pytest.raises(AccessError) as d:
        assert(message.send('32932', 1, 'Testing the error.'))

def test_authorization_change():
    assert(auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name') == {'u_id' : 1, 'token' : '12345'})
    assert(channels.create('12345', 'WorkChannelTest', False) == {'channel_id' : 1})
    with pytest.raises(AccessError) as f:
        assert(message.send('12345', 1, 'Text Example'))
    channel.invite('12345', 1, 1)
    assert(message.send('12345', 1, 'Hello World!'))

def test_inputErrors():
    pass
