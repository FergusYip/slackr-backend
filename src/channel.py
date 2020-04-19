'''
Functions to provide channel management services to the program. Will allow
users to join, invite, leave, view details, view messages, and manage owners.
'''

from error import AccessError, InputError
from token_validation import decode_token
from data_store import DATA_STORE


def channel_invite(token, channel_id, u_id):
    ''' Invite a user into a channel.

    Parameters:
        token (str): JWT of session.
        channel_id (int): ID of channel to be invited into.
        u_id (int): ID of the user to be invited.

    Returns (dict):
        empty dictionary.
    '''

    if None in {token, channel_id, u_id}:
        raise InputError(description='Insufficient parameters')

    channel_id = int(channel_id)
    channel = DATA_STORE.get_channel(channel_id)

    u_id = int(u_id)
    invitee = DATA_STORE.get_user(u_id)

    token_data = decode_token(token)
    inviter = DATA_STORE.get_user(token_data['u_id'])

    if channel is None:
        raise InputError(description='Channel does not exist')

    if invitee is None:
        raise InputError(description='User does not exist')

    if channel.is_member(inviter) is False:
        raise AccessError(
            description='The authorised user is not a member of the channel')

    if channel.is_member(invitee) is False:
        invitee.add_channel(channel)
        channel.add_member(invitee)

    return {}


def channel_details(token, channel_id):
    ''' Provides relavant data of channel.

    Parameters:
        token (str): JWT of session.
        channel_id (int): ID of the channel desired.

    Returns (dict):
        name (str): Name of channel.
        owner_members (list): list of user IDs of owner members.
        all_members (list): list of user IDs of all members.
    '''

    if None in {token, channel_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)

    u_id = int(token_data['u_id'])
    user = DATA_STORE.get_user(u_id)

    channel_id = int(channel_id)
    channel = DATA_STORE.get_channel(channel_id)

    # if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # if user asking for details is not in the channel.
    if channel.is_member(user) is False:
        raise AccessError(
            description='The authorised user is not a member of the channel')

    return channel.details


def channel_messages(token, channel_id, start):
    ''' Returns 50 messages from start.

    Parameters:
        token (str): JWT of session.
        channel_id (int): ID of channel desired.
        start (int): start index of messages.

    Returns (dict):
        messages (list): list of 50 messages from start.
        start (int): starting index of messages.
        end (int): ending index of messages, -1 if last message reached.
    '''

    if None in {token, channel_id, start}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    user = DATA_STORE.get_user(token_data['u_id'])

    channel_id = int(channel_id)
    channel = DATA_STORE.get_channel(channel_id)

    start = int(start)

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    if start > len(channel.messages) or start < 0:
        raise InputError(description='Invalid start value')

    # access error when authorized user not a member of channel.
    if channel.is_member(user) is False:
        raise AccessError(
            description='The authorised user is not a member of the channel')

    end = start + 50

    messages = []
    for i in range(50):
        try:
            message = channel.messages[start + i]
            messages.append(message.details(user))
        except IndexError:
            end = -1
            break

    return {'messages': messages, 'start': start, 'end': end}


def channel_leave(token, channel_id):
    ''' Removes user from channel.

    Parameters:
        token (str): JWT of session.
        channel_id (int): ID of channel to leave.

    Returns (dict):
        Empty dictionary.
    '''

    if None in {token, channel_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    user = DATA_STORE.get_user(token_data['u_id'])

    channel_id = int(channel_id)
    channel = DATA_STORE.get_channel(channel_id)

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # access error when authorized user not a member of channel.
    if channel.is_member(user) is False:
        raise AccessError(
            description='The authorised user is not a member of the channel')

    if user in channel.all_members:
        channel.remove_member(user)

    if user in channel.owner_members:
        channel.remove_owner(user)

    if channel in user.channels:
        user.remove_channel(channel)

    return {}


def channel_join(token, channel_id):
    ''' Adds user into channel.

    Parameters:
        token (str): JWT of session.
        channel_id (int): ID of channel to join.

    Returns:
        Empty dictionary.
    '''

    if None in {token, channel_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    user = DATA_STORE.get_user(token_data['u_id'])

    channel_id = int(channel_id)
    channel = DATA_STORE.get_channel(channel_id)

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # access error when channel is private.
    if channel.is_public is False:
        raise AccessError(description='Channel is private.')

    # Add user to channel if user is not already a member.
    if channel.is_member(user) is False:
        channel.add_member(user)

    if channel not in user.channels:
        user.add_channel(channel)

    return {}


def channel_addowner(token, channel_id, u_id):
    ''' Adds user as owner of channel.

    Parameters:
        token (str): JWT of session.
        channel_id (int): ID of channel desired.
        u_id (int): ID of user to be added as owner.

    Returns (dict):
        Empty dictionary.
    '''

    if None in {token, channel_id, u_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    admin = DATA_STORE.get_user(token_data['u_id'])

    channel_id = int(channel_id)
    channel = DATA_STORE.get_channel(channel_id)

    u_id = int(u_id)
    user = DATA_STORE.get_user(u_id)

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # input error when user does not exist.
    if user is None:
        raise InputError(description='User does not exist.')

    # input error if user already an owner of channel.
    if channel.is_owner(user) is True:
        raise InputError(description='User already owner of channel.')

    # access error when authorized user not owner of channel or owner of slackr.
    if not DATA_STORE.is_admin(admin) and not channel.is_owner(admin):
        raise AccessError(
            description='The authorised user is not an owner of the channel')

    if channel.is_member(user) is False:
        raise InputError(
            description='The authorised user is not a member of the channel')

    channel.add_owner(user)

    return {}


def channel_removeowner(token, channel_id, u_id):
    ''' Removes user as owner of channel.

    Parameters:
        token (str): JWT of session.
        channel_id (int): ID of channel desired.
        u_id (int): ID of user to be removed as owner.

    Returns (dict):
        Empty dictionary.
    '''
    if None in {token, channel_id, u_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    admin = DATA_STORE.get_user(token_data['u_id'])

    channel_id = int(channel_id)
    channel = DATA_STORE.get_channel(channel_id)

    u_id = int(u_id)
    user = DATA_STORE.get_user(u_id)

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # input error when user does not exist.
    if user is None:
        raise InputError(description='User does not exist.')

    # input error when user is not an owner
    if channel.is_owner(user) is False:
        raise InputError(
            description='The authorised user is not an owner of the channel')

    # access error when authorized user not owner of channel or owner of slackr.
    if not DATA_STORE.is_admin(admin) and not channel.is_owner(admin):
        raise AccessError(
            description='The authorised user is not a member of the channel')

    channel.remove_owner(user)

    return {}


if __name__ == '__main__':
    pass
