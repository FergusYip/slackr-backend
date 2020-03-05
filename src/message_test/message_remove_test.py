# Importing specific files for use of their functions.
import channels
import channel
import message
from error import AccessError
from error import InputError
import pytest
import auth

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
