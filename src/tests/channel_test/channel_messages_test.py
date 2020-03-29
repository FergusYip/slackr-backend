'''
System tests for channel messages function.
'''

import pytest
import channel
import channels
import auth
import message
from error import InputError
from error import AccessError

# ================================= MAKING USERS ====================================


# Making a dummy user (dummy_user1) with valid details.
@pytest.fixture
def dummy_user1():
    '''
    Pytest fixture for a dummy user for testing.
    '''

    dummy_user1 = auth.auth_register('something.else@domain.com',
                                     'GreatPassword04', 'something', 'else')
    return dummy_user1


# Making another dummy user (dummy_user2) with valid details.
@pytest.fixture
def dummy_user2():
    '''
    Pytest fixture for a dummy user for testing.
    '''

    dummy_user2 = auth.auth_register('dummy.user@domain.com',
                                     'BetterPassword09', 'dummy', 'user')
    return dummy_user2


# Making another dummy user (dummy_user3) with valid details.
@pytest.fixture
def dummy_user3():
    '''
    Pytest fixture for a dummy user for testing.
    '''

    dummy_user3 = auth.auth_register('dummy.user3@domain.com',
                                     'ReallCoolPassword9800!', 'dummy',
                                     'three')
    return dummy_user3


# ================================= MAKING CHANNELS ====================================


# Making a dummy channel (channel1) with valid details.
@pytest.fixture
def channel1(dummy_user1):  # pylint: disable=W0621
    '''
    Pytest fixture for a dummy channel for testing.
    '''

    c_id1 = channels.channels_create(dummy_user1['token'], 'name1', True)
    return c_id1


# Making another dummy channel (channel2) with valid details.
@pytest.fixture
def channel2(dummy_user2):  # pylint: disable=W0621
    '''
    Pytest fixture for a dummy channel for testing.
    '''

    c_id2 = channels.channels_create(dummy_user2['token'], 'name2', True)
    return c_id2


# Making a private dummy channel (channel_priv) with valid details.
@pytest.fixture
def channel_priv(dummy_user3):  # pylint: disable=W0621
    '''
    Pytest fixture for a dummy channel for testing.
    '''

    c_priv = channels.channels_create(dummy_user3['token'], 'name3', False)
    return c_priv


# ===================================================================================
# testing channel_messages function.
# ===================================================================================


def test_messages_sent(reset, dummy_user1, dummy_user2, channel1):  # pylint: disable=W0621
    '''
    Testing the message send function in a public channel.
    '''

    channel.channel_invite(dummy_user1['token'], channel1['channel_id'],
                           dummy_user2['u_id'])

    message.message_send(dummy_user1['token'], channel1['channel_id'],
                         "Im Batman")

    message.message_send(dummy_user2['token'], channel1['channel_id'],
                         "yeah right")

    # Getting the history of messages from 0 to 50 (by default) and checking if the
    # length of the history is 2.
    history = channel.channel_messages(dummy_user1['token'],
                                       channel1['channel_id'], 0)

    assert len(history['messages']) == 2

    assert history['start'] == 0


def test_messages_remove(reset, dummy_user1, dummy_user2, channel1):  # pylint: disable=W0621  # pylint: disable=W0621
    '''
    Testing messages function after removal.
    '''

    channel.channel_invite(dummy_user1['token'], channel1['channel_id'],
                           dummy_user2['u_id'])

    message.message_send(dummy_user1['token'], channel1['channel_id'],
                         "Im Batman")

    # message send returns dictionary with message id.
    message_id = message.message_send(dummy_user2['token'],
                                      channel1['channel_id'], "yeah right")

    message.message_remove(dummy_user2['token'], message_id['message_id'])

    history = channel.channel_messages(dummy_user2['token'],
                                       channel1['channel_id'], 0)

    assert len(history['messages']) == 1


def test_messages_id(reset, dummy_user1):  # pylint: disable=W0621  # pylint: disable=W0621
    '''
    Testing channel messages when invalid channel id is passed.
    '''

    with pytest.raises(InputError):
        channel.channel_messages(dummy_user1['token'], -1, 0)


def test_messages_start(reset, dummy_user1, channel1):  # pylint: disable=W0621  # pylint: disable=W0621
    '''
    Testing channel messages when invalid start is passed.
    '''

    message.message_send(dummy_user1['token'], channel1['channel_id'],
                         "I walk")

    message.message_send(dummy_user1['token'], channel1['channel_id'], "a")

    message.message_send(dummy_user1['token'], channel1['channel_id'],
                         "lonely road")

    history = channel.channel_messages(dummy_user1['token'],
                                       channel1['channel_id'], 0)

    with pytest.raises(InputError):
        channel.channel_messages(dummy_user1['token'], channel1['channel_id'],
                                 len(history['messages']) + 1)


def test_messages_access(reset, dummy_user1, channel2):  # pylint: disable=W0621  # pylint: disable=W0621
    '''
    Checking for an AccessError when a user asks for message history of a channel
    that he is not a member of.
    '''

    with pytest.raises(AccessError):
        channel.channel_messages(dummy_user1['token'], channel2['channel_id'],
                                 0)


def test_messages_invalid_token(reset, channel1, invalid_token):  # pylint: disable=W0621  # pylint: disable=W0621
    '''
    Testing case when the token passed into the channel_messages() function is invalid.
    '''

    with pytest.raises(AccessError):
        channel.channel_messages(invalid_token, channel1['channel_id'], 0)


def test_messages_insufficient_params(reset):
    '''Test input of invalid parameters into messages'''

    with pytest.raises(InputError):
        channel.channel_messages(None, None, None)
