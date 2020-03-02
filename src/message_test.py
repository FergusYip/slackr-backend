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
def test_message_send():
    # Creating a new user.
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    # Creating a new channel.
    channel_id = channels.create(new_user['token'], 'Channel1', True)
    # Creating a variable 'new_message' to hold the dictionary return from the send function.
    new_message = message.send(new_user['token'], channel_id['channel_id'], 'Hello world!')
    # 'messages' will hold the list of dictionary information for the most recent 50 messages.
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0)
    # Ensuring the most recent message's id matches the one send from new_user
    assert(new_message['message_id'] == messages[0]['message_id'])

# Testing unauthorized sending of messages.
def test_unauthorized():
    # Creating a new user to test the function with.
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    # Creating a second user to test this function with.
    second_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    # 'new_user' creates this channel that is PRIVATE.
    channel_id = channels.create(new_user['token'], 'Channel2', False)
    # An AccessError should be raised if 'second_user' attempts to send a message in this private channel
    with pytest.raises(AccessError) as e:
        message.send(second_user['token'], channel_id['channel_id'], 'Hello team')

# Testing a change in authorization affecting message sending.
def test_authorization_change():
    # Creating 2 new users and having 'new_user' create a new channel.
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.register('letmein@test.com', 'Password1', 'Sample', 'Name')
    channel_id = channels.create(new_user['token'], 'Channel3', False)
    # The second_user should initially be unable to send a message in this channel.
    with pytest.raises(AccessError) as e:
        message.send(second_user['token'], channel_id['channel_id'], 'Why wont this send?')
    # 'new_user' invites the 'second_user' to this new channel.
    channel.invite(new_user['token'], channel_id['channel_id'], second_user['u_id'])
    # Creating variables to hold the dictionary returns for both functions.
    new_message = message.send(second_user['token'], channel_id['channel_id'], 'Hello World!')
    messages = channel.messages(second_user['token'], channel_id['channel_id'], 0)
    # Asserting the most recent message in the channel's id matches the id sent from the user.
    assert(new_message['message_id'] == messages[0]['message_id'])

# Testing an incorrect character length string message.
def test_inputErrors():
    # Creating a new user and having them create a new channel.
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    channel_id = channels.create(new_user['token'], 'Channel4', True)
    # This should raise an error if the message length is greater than 1000.
    with pytest.raises(InputError) as e:
        message.send(new_user['token'], channel_id['channel_id'], 'i' * 1001)

def test_almostInputError():
    # Creating a new user and having them create a new channel.
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    channel_id = channels.create(new_user['token'], 'New Channel', True)
    # The message should send if the length of the message is 1000 characters.
    new_message = message.send(second_user['token'], channel_id['channel_id'], 'i' * 1000)
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0)
    # Asserting that the new message sent correctly.
    assert(new_message['message_id'] == messages[0]['message_id'])

# =====================================================
# ========== TESTING MESSAGE REMOVE FUNCTION ==========
# =====================================================

def test_messageRemove():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')

    channel_id = channels.create(new_user['token'], 'Channel5', True)

    new_message = message.send(new_user['token'], channel_id['channel_id'], 'hello world!')
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0)
    assert(new_message['message_id'] == messages[0]['message_id']) # Ensure the message sent

    message.remove(new_user['token'], new_message['message_id'])

    assert(new_message['message_id'] != messages[0]['message_id'])

def test_messageInputError():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')

    channel_id = channels.create(new_user['token'], 'Channel6', True)

    with pytest.raises(InputError) as e:
            message.remove(new_user['token'], 1) # Random message ID to remove.

def test_OneRemoveOneFail():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')

    channel_id = channels.create(new_user['token'], 'Channel7', True)

    new_message = message.send(new_user['token'], channel_id['channel_id'], 'hello world!')
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0)
    assert(new_message['message_id'] == messages[0]['message_id']) # Ensure the message sent

    second_message = message.send(new_user['token'], channel_id['channel_id'], 'hello slackr you mean')
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0)
    assert(new_message['message_id'] == messages[0]['message_id']) # Ensure the message sent correctly.

    message.remove(new_user['token'], second_message['message_id']) # Removing the 2nd message.
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0) # Update the messages variable.

    assert(new_message['message_id'] == messages[0]['message_id']) # Ensure the recent message was removed from the front of the list.

    message.remove(new_user['token'], new_message['message_id'])
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0) # Update the messages variable.

    assert(new_message['message_id'] != messages[0]['message_id']) # Ensure both messages were removed from the front of the list.

def test_unauthorizedRemoval(): # Person unauthorized for a channel attempting to remove a message.
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.register('test2@test.com', 'PaSsWoRd1', 'Dummy', 'Name')

    channel_id = channels.create(new_user['token'], 'Channel8', False)
    new_message = message.send(new_user['token'], channel_id['channel_id'], 'removemepls')

    with pytest.raises(AccessError) as e:
        message.remove(second_user['token'], new_message['message_id'])

def test_unauthorizedRemoval2():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.register('test2@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    # The channel is public now.
    channel_id = channels.create(new_user['token'], 'Channel9', True)
    # Second_user is not the owner/admin of this channel.
    new_message = message.send(new_user['token'], channel_id['channel_id'], 'Hello World!')

    with pytest.raises(AccessError) as e:
        message.remove(second_user['token'], new_message['message_id'])

def test_unauthorizedRemoval3():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.register('test2@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    # New user has made this channel. (Is the channel owner)
    channel_id = channels.create(new_user['token'], 'Channel10', True)

    new_message = message.send(second_user['token'], channel_id['channel_id'], 'Hello Earth!')
    message.remove(new_user['token'], new_message['message_id']) # New_user can remove this message as they are the owner.
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0) # Update the messages variable.

    assert(new_message['message_id'] != messages[0]['message_id']) # Asserting the message was removed properly.

def test_changeOwners():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.register('test2@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    # New user has made this channel. (Is the channel owner)
    channel_id = channels.create(new_user['token'], 'Channel10', True)
    channel.addowner(new_user['token'], channel_id['channel_id'], second_user['u_id'])

    new_message = message.send(new_user['token'], channel_id['channel_id'], 'Hello Earth!')
    message.remove(second_user['token'], new_message['message_id'])

    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0) # Update the messages list.

    assert(new_message['message_id'] != messages[0]['message_id']) # Asserting the removal was successful.

# =====================================================
# ========== TESTING MESSAGE EDIT FUNCTION ============
# =====================================================

def test_averageCaseEdit():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    channel_id = channels.create(new_user['token'], 'Channel10', True)

    new_message = message.send(new_user['token'], channel_id['channel_id'], 'Your good at programming')
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0) # Update the messages variable.

    # Ensure that the message sent correctly before testing.
    assert(new_message['message_id'] != messages[0]['message_id']) # Asserting the message was removed properly.

    message.edit(new_user['token'], new_message['message_id'], "You're** Oops spelling")
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0) # Update the messages variable.

    assert("You're** Oops spelling" == messages[0]['message']) # Ensure the edited message is displayed.


def test_emptyStringDelete():
    new_user = auth.register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    channel_id = channels.create(new_user['token'], 'Channel10', True)

    new_message = message.send(new_user['token'], channel_id['channel_id'], 'I dont like you anymore')
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0) # Update the messages variable.

    # Ensure that the message sent correctly before testing.
    assert(new_message['message_id'] != messages[0]['message_id']) # Asserting the message was removed properly.

    message.edit(new_user['token'], new_message['message_id'], "")
    messages = channel.messages(new_user['token'], channel_id['channel_id'], 0) # Update the messages variable.

    assert(new_message['message_id'] != messages[0]['message_id']) # Ensure the edited message is deleted and no longer the most recent message.


def test_AccessErrorUnauthorized():
    pass

def test_AccessErrorOwner():
    pass
