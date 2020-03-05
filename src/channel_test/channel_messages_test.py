import channel
import channels
import pytest
import auth
import message
from error import InputError
from error import AccessError

# ================================= MAKING USERS ====================================

# Making a dummy user (dummy_user1) with valid details.
@pytest.fixture
def dummy_user1():
    dummy_user1 = auth.auth_register(
        'something.else@domain.com', 'GreatPassword04', 'something', 'else')
    return dummy_user1


# Making another dummy user (dummy_user2) with valid details.
@pytest.fixture
def dummy_user2():
    dummy_user2 = auth.auth_register(
        'dummy.user@domain.com', 'BetterPassword09', 'dummy', 'user')
    return dummy_user2

# Making another dummy user (dummy_user3) with valid details.
@pytest.fixture
def dummy_user3():
    dummy_user3 = auth.auth_register(
        'dummy.user3@domain.com', 'ReallCoolPassword9800!', 'dummy', 'three')
    return dummy_user3


# ================================= MAKING CHANNELS ====================================


# Making a dummy channel (channel1) with valid details.
@pytest.fixture
def channel1(dummy_user1):
    c_id1 = channels.channels_create(dummy_user1['token'], 'name1', True)
    return c_id1


# Making another dummy channel (channel2) with valid details.
@pytest.fixture
def channel2(dummy_user2):
    c_id2 = channels.channels_create(dummy_user2['token'], 'name2', True)
    return c_id2


# Making a private dummy channel (channel_priv) with valid details.
@pytest.fixture
def channel_priv(dummy_user3):
    c_priv = channels.channels_create(dummy_user3['token'], 'name3', False)
    return c_priv


# ===================================================================================
# testing channel_messages function.
# ===================================================================================


def test_messages_sent(dummy_user1, dummy_user2, channel1):
    '''
    dummy_user1 sends a message into channel1 and then dummy_user2 sends a reply.
    assert that the length of the message history is now 2.
    assert that the start value is actually 0.
    '''

    channel.channel_invite(
        dummy_user1['token'], channel1['channel_id'], dummy_user2['u_id'])

    message.message_send(
        dummy_user1['token'], channel1['channel_id'], "Im Batman")

    message.message_send(
        dummy_user2['token'], channel1['channel_id'], "yeah right")

    # Getting the history of messages from 0 to 50 (by default) and checking if the length of the history is 2.
    history = channel.channel_messages(
        dummy_user1['token'], channel1['channel_id'], 0)

    assert len(history['messages']) == 2

    assert(history['start'] == 0)


def test_messages_remove(dummy_user2, channel2):
    '''
    dummy_user2 sends another message, then removes it. 
    assert that the length of the message history is still 2.
    '''

    message_id = message.message_send(
        dummy_user2['token'], channel2['channel_id'], "idk why I talk to you.")

    message.message_remove(dummy_user2['token'], message_id['message_id'])

    history = channel.channel_messages(
        dummy_user2['token'], channel2['channel_id'], 0)

    assert len(history['messages']) == 0


def test_messages_id(dummy_user1):
    '''
    Checking for an InputError when an invalid channel_id is passed into the 
    channel_messages function.
    '''

    with pytest.raises(InputError):
        channel.channel_messages(dummy_user1['token'], 31415926, 0)


def test_messages_start(dummy_user1, channel1):
    '''
    Checking for an InputError when the channel_messages function get a start
    that is greater than the size of the message history
    '''
    message.message_send(dummy_user1['token'],
                         channel1['channel_id'], "I walk")
    message.message_send(dummy_user1['token'], channel1['channel_id'], "a")
    message.message_send(dummy_user1['token'],
                         channel1['channel_id'], "lonely road")

    history = channel.channel_messages(
        dummy_user1['token'], channel1['channel_id'], 0)

    with pytest.raises(InputError):
        channel.channel_messages(
            dummy_user1['token'], channel1['channel_id'], len(history['messages']) + 1)


def test_messages_access(dummy_user1, channel2):
    '''
    Checking for an AccessError when a user asks for message history of a channel
    that he is not a member of.
    '''

    with pytest.raises(AccessError):
        channel.channel_messages(
            dummy_user1['token'], channel2['channel_id'], 0)


def test_invalid_token_messages(dummy_user1, channel1, invalid_token):
    with pytest.raises(AccessError):
        channel.channel_messages(invalid_token, channel1['channel_id'], 0)
