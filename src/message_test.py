# Testing the message.py file

import message

# Simple tests of average case messages.
def test_message_send():
    assert(message.send('12345', 6, 'Hello world!') == {'message_id' : 1})
    assert(message.send('22342', 1, 'testingamessagenospaces') == {'message_id' : 1})
    assert(message.send('32982', 37, '12176182812') == {'message_id' : 1})
    
