'''
Functions to provide channel management services to the program. Will allow
users to join, invite, leave, view details, view messages, and manage owners.
'''

from slackr import db
from slackr.error import AccessError, InputError
from slackr.models.channel import Channel
from slackr.models.user import User
from slackr.token_validation import decode_token
from slackr.utils.constants import PERMISSIONS


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

    token_data = decode_token(token)
    inviter = User.query.get(token_data['u_id'])
    invitee = User.query.get(u_id)
    channel = Channel.query.get(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist')

    if invitee is None:
        raise InputError(description='User does not exist')

    if channel.is_member(inviter) is False:
        raise AccessError(
            description='The authorised user is not a member of the channel')

    if channel.is_member(invitee) is False:
        channel.all_members.append(invitee)
        db.session.commit()

    return {
        'channel': {
            'channel_id': channel.channel_id,
            'name': channel.name,
            'is_public': channel.is_public
        },
        'user': invitee.details
    }


def channel_details(token, channel_id):
    ''' Provides relevant data of channel.

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
    user = User.query.get(int(token_data['u_id']))
    channel = Channel.query.get(int(channel_id))

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
    user = User.query.get(int(token_data['u_id']))
    channel = Channel.query.get(int(channel_id))

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

    sent_messages = [m for m in channel.messages if not m.is_hidden]
    sent_messages.sort(key=lambda m: m.time_created)

    messages = []
    for i in range(50):
        try:
            message = sent_messages[start + i]
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
    user = User.query.get(int(token_data['u_id']))
    channel = Channel.query.get(int(channel_id))

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # access error when authorized user not a member of channel.
    if channel.is_member(user) is False:
        raise AccessError(
            description='The authorised user is not a member of the channel')

    if user in channel.all_members:
        channel.all_members.remove(user)

    if user in channel.owner_members:
        channel.owner_members.remove(user)

    db.session.commit()

    return {
        'channel': {
            'channel_id': channel.channel_id,
            'name': channel.name,
            'is_public': channel.is_public
        },
        'user': user.details
    }


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
    user = User.query.get(int(token_data['u_id']))

    channel_id = int(channel_id)
    channel = Channel.query.get(int(channel_id))

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # access error when channel is private.
    if channel.is_public is False:
        raise AccessError(description='Channel is private.')

    # Add user to channel if user is not already a member.
    if channel.is_member(user) is False:
        channel.all_members.append(user)
        db.session.commit()

    return {
        'channel': {
            'channel_id': channel.channel_id,
            'name': channel.name,
            'is_public': channel.is_public
        },
        'user': user.details
    }


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
    admin = User.query.get(token_data['u_id'])
    channel = Channel.query.get(int(channel_id))
    user = User.query.get(u_id)

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
    if admin.permission_id != PERMISSIONS['owner'] and not channel.is_owner(
            admin):
        raise AccessError(
            description='The authorised user is not an owner of the channel')

    if channel.is_member(user) is False:
        raise InputError(
            description='The authorised user is not a member of the channel')

    channel.owner_members.append(user)
    db.session.commit()

    return user.details


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
    admin = User.query.get(token_data['u_id'])

    channel_id = int(channel_id)
    channel = Channel.query.get(int(channel_id))
    user = User.query.get(int(u_id))

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
    if admin.permission_id != PERMISSIONS['owner'] and not channel.is_owner(
            admin):
        raise AccessError(
            description='The authorised user is not a member of the channel')

    channel.owner_members.remove(user)
    db.session.commit()

    return user.details


if __name__ == '__main__':
    pass
