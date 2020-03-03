# Testing the message.py file

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

# =====================================================
# ========== TESTING MESSAGE REMOVE FUNCTION ==========
# =====================================================

def test_messageRemove():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    channel_id = channels.channels_create(new_user['token'], 'Channel5', True)
    new_message = message.message_send(new_user['token'], channel_id['channel_id'], 'hello world!')
    message.message_remove(new_user['token'], new_message['message_id'])

def test_removeTwo():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    channel_id = channels.channels_create(new_user['token'], 'Channel7', True)

    new_message = message.message_send(new_user['token'], channel_id['channel_id'], 'hello world!')
    second_message = message.message_send(new_user['token'], channel_id['channel_id'], 'hello slackr you mean')

    message.message_remove(new_user['token'], second_message['message_id']) # Removing the 2nd message.
    message.message_remove(new_user['token'], new_message['message_id'])

def test_messageremove_wrongID():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    channel_id = channels.channels_create(new_user['token'], 'Channel6', True)
    with pytest.raises(InputError) as e:
            message.message_remove(new_user['token'], 99999) # Random message ID to remove.

def test_unauthorizedRemoval(): # Person unauthorized for a channel attempting to remove a message.
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.auth_register('test2@test.com', 'PaSsWoRd1', 'Dummy', 'Name')

    channel_id = channels.channels_create(new_user['token'], 'Channel8', True)
    new_message = message.message_send(new_user['token'], channel_id['channel_id'], 'removemepls')
    with pytest.raises(AccessError) as e:
        message.message_remove(second_user['token'], new_message['message_id'])

def test_ownerRemoval():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.auth_register('test2@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    # New user has made this channel. (Is the channel owner)
    channel_id = channels.channels_create(new_user['token'], 'Channel10', True)
    channel.channel_invite(new_user['token'], channel_id['channel_id'], second_user['u_id'])
    new_message = message.message_send(second_user['token'], channel_id['channel_id'], 'Hello Earth!')
    message.message_remove(new_user['token'], new_message['message_id']) # New_user can remove this message as they are the owner.

def test_changeOwners():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.auth_register('test2@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    # New user has made this channel. (Is the channel owner)
    channel_id = channels.channels_create(new_user['token'], 'Channel11', True)
    channel.channel_invite(new_user['token'], channel_id['channel_id'], second_user['u_id'])
    channel.channel_addowner(new_user['token'], channel_id['channel_id'], second_user['u_id'])
    new_message = message.message_send(new_user['token'], channel_id['channel_id'], 'Hello Earth!')
    message.message_remove(second_user['token'], new_message['message_id'])

# =====================================================
# ========== TESTING MESSAGE EDIT FUNCTION ============
# =====================================================

def test_averageCaseEdit():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    channel_id = channels.channels_create(new_user['token'], 'Channel12', True)
    new_message = message.message_send(new_user['token'], channel_id['channel_id'], 'Your good at programming')
    message.message_edit(new_user['token'], new_message['message_id'], "You're** Oops spelling")

def test_emptyStringDelete():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    channel_id = channels.channels_create(new_user['token'], 'Channel13', True)
    new_message = message.message_send(new_user['token'], channel_id['channel_id'], 'I dont like you anymore')
    message.message_edit(new_user['token'], new_message['message_id'], "")

    messages = channel.channel_messages(new_user['token'], channel_id['channel_id'], 0) # Update the messages variable.
    assert(new_message['message_id'] != messages[0]['message_id']) # Ensure the edited message is deleted and no longer the most recent message.

def test_OwnerEdit():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.auth_register('tester2@test.com', 'Password42', 'Lorem', 'Ipsum')
    # Creating a private channel that second_user cannot access.
    channel_id = channels.channels_create(new_user['token'], 'Channel16', True)
    channel.channel_invite(new_user['token'], channel_id['channel_id'], second_user['u_id'])
    new_message = message.message_send(second_user['token'], channel_id['channel_id'], 'edit me')
    message.message_edit(new_user['token'], new_message['message_id', "hello there"])

def test_AccessErrorUnauthorized():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.auth_register('anotheremail@gmail.com', 'Password', 'Lorem', 'Ipsum')
    channel_id = channels.channels_create(new_user['token'], 'Channel15', True)
    channel.channel_invite(new_user['token'], channel_id['channel_id'], second_user['u_id'])
    new_message = message.message_send(new_user['token'], channel_id['channel_id'], 'Hola el mundo!')

    with pytest.raises(AccessError) as e:
        message.message_edit(second_user['token'], new_message['message_id'], "el ladron!")

def test_AccessErrorNotAdmin():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.auth_register('anotheremail@gmail.com', 'Password', 'Lorem', 'Ipsum')
    third_user = auth.auth_register('wow@gmail.com', 'Password', 'CreativeName', 'Generator')

    channel_id = channels.channels_create(new_user['token'], 'Channel15', True)
    channel.channel_invite(new_user['token'], channel_id['channel_id'], second_user['u_id'])
    channel.channel_invite(new_user['token'], channel_id['channel_id'], third_user['u_id'])
    new_message = message.message_send(second_user['token'], channel_id['channel_id'], 'Bienvenidos!')
    with pytest.raises(AccessError) as e:
        message.message_edit(third_user['token'], new_message['message_id'], "el ladron!")
