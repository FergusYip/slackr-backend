# Importing specific files for use of their functions.
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

# Simple tests of average case messages.
def test_averagecase_send():
    # Creating a new user.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    # Creating a new channel.
    channel_id = channels.channels_create(new_user['token'], 'Channel1', True)
    # Creating a variable 'new_message' to hold the dictionary return from the send function.
    new_message = message.message_send(new_user['token'], channel_id['channel_id'], 'Hello world!')

# Testing unauthorized sending of messages.
def test_sendunauthorized():
    # Creating a new user to test the function with.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    # Creating a second user to test this function with.
    second_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    # 'new_user' creates this channel that is PRIVATE.
    channel_id = channels.channels_create(new_user['token'], 'Channel2', True)
    # An AccessError should be raised if 'second_user' attempts to send a message in this channel
    with pytest.raises(AccessError) as e:
        message.message_send(second_user['token'], channel_id['channel_id'], 'Hello team')

# Testing a change in authorization affecting message sending.
def test_sendauthorization_change():
    # Creating 2 new users and having 'new_user' create a new channel.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.auth_register('letmein@test.com', 'Password1', 'Sample', 'Name')
    channel_id = channels.channels_create(new_user['token'], 'Channel3', True)
    # The second_user should initially be unable to send a message in this channel.
    with pytest.raises(AccessError) as e:
        message.message_send(second_user['token'], channel_id['channel_id'], 'Why wont this send?')
    # 'new_user' invites the 'second_user' to this new channel.
    channel.channel_invite(new_user['token'], channel_id['channel_id'], second_user['u_id'])
    # Creating variables to hold the dictionary returns for both functions.
    message.message_send(second_user['token'], channel_id['channel_id'], 'Hello World!')

# Testing an incorrect character length string message.
def test_sendonethousandandone():
    # Creating a new user and having them create a new channel.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    channel_id = channels.channels_create(new_user['token'], 'Channel4', True)
    # This should raise an error if the message length is greater than 1000.
    with pytest.raises(InputError) as e:
        message.message_send(new_user['token'], channel_id['channel_id'], 'i' * 1001)

def test_onethousandchars():
    # Creating a new user and having them create a new channel.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    channel_id = channels.channels_create(new_user['token'], 'New Channel', True)
    # The message should send if the length of the message is 1000 characters.
    new_message = message.message_send(second_user['token'], channel_id['channel_id'], 'i' * 1000)
