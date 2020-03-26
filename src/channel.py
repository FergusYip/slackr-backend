'''
Implementing channel functions -
invite, details, messages, leave, join, addowner, removeowner
'''

from json import dumps
from flask import request, Blueprint
from error import AccessError, InputError
from data_store import data_store
from token_validation import decode_token

CHANNEL = Blueprint('channel', __name__)


@CHANNEL.route("/channel/invite", methods=['POST'])
def route_channel_invite():
    '''
    Flask route to implement channel_invite function.
    '''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    return dumps(channel_invite(token, channel_id, u_id))


@CHANNEL.route("/channel/details", methods=['GET'])
def route_channel_details():
    '''
    Flask route to implement channel_invite function.
    '''
    token = request.values.get('token')
    channel_id = request.values.get('channel_id')
    return dumps(channel_details(token, channel_id))


@CHANNEL.route("/channel/messages", methods=['GET'])
def route_channel_messages():
    '''
    Flask route for channel_messages function.
    '''
    token = request.values.get('token')
    channel_id = request.values.get('channel_id')
    start = request.values.get('start')
    return dumps(channel_messages(token, channel_id, start))


@CHANNEL.route("/channel/leave", methods=['POST'])
def route_channel_leave():
    '''
    Flask route to implement channel_leave function.
    '''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    return dumps(channel_leave(token, channel_id))


@CHANNEL.route("/channel/join", methods=['POST'])
def route_channel_join():
    '''
    Flask route for channel_join function.
    '''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    return dumps(channel_join(token, channel_id))


@CHANNEL.route("/channel/addowner", methods=['POST'])
def route_channel_addowner():
    '''
    Flask route for channel_addowner function.
    '''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    return dumps(channel_addowner(token, channel_id, u_id))


@CHANNEL.route("/channel/removeowner", methods=['POST'])
def route_channel_removeowner():
    '''
    Implementing removeowner function by removing user from channel['owner_members']
    '''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    return dumps(channel_removeowner(token, channel_id, u_id))


def channel_invite(token, channel_id, u_id):
    '''
    Invite a user into a channel with ID channel_id
    '''
    if None in {token, channel_id, u_id}:
        raise InputError(description='Insufficient parameters')

    channel_id = int(channel_id)
    u_id = int(u_id)

    decode_token(token)

    if data_store.get_user(u_id) is None:
        raise InputError(description='User does not exist.')

    channel = data_store.get_channel(channel_id)
    invitee = data_store.get_user(u_id)

    if invitee not in channel.all_members:
        channel.add_member(invitee)

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

    # input error when the given start is greater than the id of last message.
    if start > len(channel['messages']):
        raise InputError(description='start is greater than end')

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # access error when authorized user not a member of channel.
    if channel.is_member(user) is False:
        raise AccessError(
            description='authorized user not a member of channel.')

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
