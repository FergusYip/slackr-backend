# Testing the message.py file

import channels
import message
from error import AccessError
import pytest

# Simple tests of average case messages.
def test_message_send():
    assert(message.send('12345', 6, 'Hello world!') == {'message_id' : 1})
    assert(message.send('22342', 1, 'testingamessagenospaces') == {'message_id' : 1})
    assert(message.send('32982', 37, '12176182812') == {'message_id' : 1})
    
def test_unauthorized():    
    assert(channels.create('12345', 'areyouallowedin', False) == {'channel_id' : 1})    
    with pytest.raises(AccessError) as e:
        assert(message.send('12345', 1, 'Hello team'))
    
