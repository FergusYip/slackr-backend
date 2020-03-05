# Importing specific files for use of their functions.
import channels
import channel
import message
from error import AccessError
from error import InputError
import pytest
import auth

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

def test_AccessErrorNotOwner():
    new_user = auth.auth_register('test@test.com', 'PaSsWoRd1', 'Dummy', 'Name')
    second_user = auth.auth_register('anotheremail@gmail.com', 'Password', 'Lorem', 'Ipsum')
    third_user = auth.auth_register('wow@gmail.com', 'Password', 'CreativeName', 'Generator')

    channel_id = channels.channels_create(new_user['token'], 'Channel15', True)
    channel.channel_invite(new_user['token'], channel_id['channel_id'], second_user['u_id'])
    channel.channel_invite(new_user['token'], channel_id['channel_id'], third_user['u_id'])
    new_message = message.message_send(second_user['token'], channel_id['channel_id'], 'Bienvenidos!')
    with pytest.raises(AccessError) as e:
        message.message_edit(third_user['token'], new_message['message_id'], "el ladron!")
