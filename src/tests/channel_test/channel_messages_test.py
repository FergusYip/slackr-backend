'''
System tests for channel messages function.
'''

import pytest
import channel
import message
from error import InputError
from error import AccessError


def test_messages_sent(reset, new_user, new_channel):
    '''
    Testing the message send function in a public channel.
    '''
    owner = new_user(email='owner@email.com')
    test_channel = new_channel(owner)

    message.message_send(owner['token'], test_channel['channel_id'],
                         "Im Batman")

    message.message_send(owner['token'], test_channel['channel_id'],
                         "yeah right")

    # Getting the history of messages from 0 to 50 (by default) and checking if the
    # length of the history is 2.
    history = channel.channel_messages(owner['token'],
                                       test_channel['channel_id'], 0)

    assert len(history['messages']) == 2

    assert history['start'] == 0


def test_messages_react(reset, new_user, new_channel):
    '''
    Testing message send function.
    '''

    user = new_user(email='user_1@email.com')
    test_channel = new_channel(user)

    msg = message.message_send(user['token'], test_channel['channel_id'],
                               'hello')

    message.message_react(user['token'], msg['message_id'], 1)

    channel_messages = channel.channel_messages(user['token'],
                                                test_channel['channel_id'], 0)

    assert len(channel_messages['messages']) == 1
    assert channel_messages['start'] == 0

    assert len(channel_messages['messages'][0]['reacts']) == 1

    react = channel_messages['messages'][0]['reacts'][0]
    assert react['react_id'] == 1


def test_messages_remove(reset, new_user, new_channel):
    '''
    Testing messages function after removal.
    '''

    owner = new_user(email='owner@email.com')
    test_channel = new_channel(owner)

    msg = message.message_send(owner['token'], test_channel['channel_id'],
                               'hello')

    messages = channel.channel_messages(owner['token'],
                                        test_channel['channel_id'], 0)

    assert len(messages['messages']) == 1

    message.message_remove(owner['token'], msg['message_id'])

    messages = channel.channel_messages(owner['token'],
                                        test_channel['channel_id'], 0)

    assert not messages['messages']


def test_messages_id(reset, test_user):
    '''
    Testing channel messages when invalid channel id is passed.
    '''

    with pytest.raises(InputError):
        channel.channel_messages(test_user['token'], -1, 0)


def test_messages_start(reset, test_user, test_channel):
    '''
    Testing channel messages when invalid start is passed.
    '''

    message.message_send(test_user['token'], test_channel['channel_id'],
                         "I walk")

    message.message_send(test_user['token'], test_channel['channel_id'], "a")

    message.message_send(test_user['token'], test_channel['channel_id'],
                         "lonely road")

    history = channel.channel_messages(test_user['token'],
                                       test_channel['channel_id'], 0)

    with pytest.raises(InputError):
        channel.channel_messages(test_user['token'],
                                 test_channel['channel_id'],
                                 len(history['messages']) + 1)


def test_messages_access(reset, new_user, test_channel):
    '''
    Checking for an AccessError when a user asks for message history of a channel
    that he is not a member of.
    '''

    stranger = new_user(email='stranger@email.com')

    with pytest.raises(AccessError):
        channel.channel_messages(stranger['token'], test_channel['channel_id'],
                                 0)


def test_messages_invalid_token(reset, test_channel, invalid_token):
    '''
    Testing case when the token passed into the channel_messages() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_messages(invalid_token, test_channel['channel_id'], 0)


def test_messages_insufficient_params(reset):
    '''Test input of invalid parameters into messages'''

    with pytest.raises(InputError):
        channel.channel_messages(None, None, None)
