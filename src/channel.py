'''
Implementing channel functions -
invite, details, messages, leave, join, addowner, removeowner
'''
from error import AccessError, InputError
from token_validation import decode_token
from data_store import data_store


def channel_invite(token, channel_id, u_id):
    '''
    Invite a user into a channel with ID channel_id
    '''

    if None in {token, channel_id, u_id}:
        raise InputError(description='Insufficient parameters')

    channel_id = int(channel_id)
    channel = data_store.get_channel(channel_id)

    u_id = int(u_id)
    invitee = data_store.get_user(u_id)

    token_data = decode_token(token)
    inviter = data_store.get_user(token_data['u_id'])

    if channel is None:
        raise InputError(description='Channel does not exist')

    if invitee is None:
        raise InputError(description='User does not exist')

    if channel.is_member(inviter) is False:
        raise AccessError(
            description='The authorised user is not a member of the channel')

    if channel.is_member(invitee) is False:
        data_store.join_channel(invitee, channel)

    return {}


def channel_details(token, channel_id):
    '''
    Implementing details function by returning json of dictionary containing
    relavant information of a channel.
    '''

    if None in {token, channel_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    u_id = int(token_data['u_id'])
    channel_id = int(channel_id)

    user = data_store.get_user(u_id)
    channel = data_store.get_channel(channel_id)

    # if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # if user asking for details is not in the channel.
    if channel.is_member(user) is False:
        raise AccessError(description='Authorized user not in the channel')

    return channel.details


def channel_messages(token, channel_id, start):
    '''
    Implementing invite function by appending user to channel['all_members']
    '''

    if None in {token, channel_id, start}:
        raise InputError(description='Insufficient parameters')

    channel_id = int(channel_id)
    start = int(start)

    token_data = decode_token(token)
    channel = data_store.get_channel(channel_id)
    user = data_store.get_user(token_data['u_id'])

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    if start > len(channel.messages) or start < 0:
        raise InputError(description='Invalid start value')

    # access error when authorized user not a member of channel.
    if channel.is_member(user) is False:
        raise AccessError(
            description='Authorized user not a member of channel.')

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
    '''
    Implementing leave function by removing user from channel['all_members']
    and channel['owner_members']
    '''

    if None in {token, channel_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    user = data_store.get_user(token_data['u_id'])

    channel_id = int(channel_id)
    channel = data_store.get_channel(channel_id)

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # access error when authorized user not a member of channel.
    if channel.is_member is False:
        raise AccessError(
            description='Authorized user not a member of channel.')

    if user in channel.all_members:
        channel.remove_member(user)

    if user in channel.owner_members:
        channel.remove_owner(user)

    if channel in user.channels:
        user.remove_channel(channel)

    return {}


def channel_join(token, channel_id):
    '''
    Implementing join function by appending user to channel['all_members']
    '''

    if None in {token, channel_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    user = data_store.get_user(token_data['u_id'])

    channel_id = int(channel_id)
    channel = data_store.get_channel(channel_id)

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
    '''
    Implementing addowner function by appending user to channel['owner_members']
    '''

    if None in {token, channel_id, u_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    admin = data_store.get_user(token_data['u_id'])

    channel_id = int(channel_id)
    channel = data_store.get_channel(channel_id)

    u_id = int(u_id)
    user = data_store.get_user(u_id)

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # input error when user does not exist.
    if user is None:
        raise InputError(description='User does not exist.')

    # input error if user already an owner of channel.
    if data_store.is_owner(user) is True:
        raise InputError(description='User already owner of channel.')

    # access error when authorized user not owner of channel or owner of slackr.
    if False in {data_store.is_admin(admin), channel.is_owner(admin)}:
        raise AccessError(description='Authorized user not owner of channel.')

    if channel.is_member(user) is False:
        channel.add_member(user)

    channel.add_owner(user)

    return {}


def channel_removeowner(token, channel_id, u_id):
    '''
    Implementing addowner function by appending user to channel['owner_members']
    '''
    if None in {token, channel_id, u_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    admin = data_store.get_user(token_data['u_id'])

    channel_id = int(channel_id)
    channel = data_store.get_channel(channel_id)

    u_id = int(u_id)
    user = data_store.get_user(u_id)

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # input error when user does not exist.
    if user is None:
        raise InputError(description='User does not exist.')

    # input error when user is not an owner
    if channel.is_owner(user) is False:
        raise InputError(description='User is not an owner of channel.')

    # access error when authorized user not owner of channel or owner of slackr.
    if False in {data_store.is_admin(admin), channel.is_owner(admin)}:
        raise AccessError(description='Authorized user not owner of channel.')

    channel.remove_owner(user)

    return {}


if __name__ == '__main__':
    pass
