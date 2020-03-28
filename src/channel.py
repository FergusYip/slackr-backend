'''
Implementing channel functions -
invite, details, messages, leave, join, addowner, removeowner
'''

from json import dumps
from flask import Flask, request, Blueprint
from flask_cors import CORS
from error import AccessError, InputError
from data_store import data_store
from token_validation import decode_token
import helpers

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

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

    token_data = decode_token(token)

    if helpers.get_user(u_id) is None:
        raise InputError(description='User does not exist.')

    if not helpers.is_channel_member(u_id, channel_id):
        add_into_channel(token_data['u_id'], channel_id, u_id)

    return {}


def add_into_channel(inviter, c_id, invited):
    '''
    Appends a user ID into the channel with ID c_id.
    '''
    for channel in data_store['channels']:
        if channel['channel_id'] == c_id:
            if inviter not in channel['all_members']:
                raise AccessError(
                    description='User does not have permission to invite')

            channel['all_members'].append(invited)


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

    user = helpers.get_user(u_id)
    channel = helpers.get_channel(channel_id)

    # if channel doesn't exist.
    if helpers.get_channel(channel_id) is None:
        raise InputError(description='Channel does not exist.')

    # if user asking for details is not in the channel.
    if helpers.is_channel_member(u_id, channel_id) is False:
        raise AccessError(description='Authorized user not in the channel')

    # finding the right channel.
    channel = helpers.get_channel(channel_id)

    owner_members = []
    for owner_id in channel['owner_members']:
        owner = helpers.get_user(owner_id)
        owner_dict = {
            'u_id': owner['u_id'],
            'name_first': owner['name_first'],
            'name_last': owner['name_last'],
        }
        owner_members.append(owner_dict)

    all_members = []
    for user_id in channel['all_members']:
        user = helpers.get_user(user_id)
        user_dict = {
            'u_id': user['u_id'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
        }
        all_members.append(user_dict)

    details = {
        'name': channel['name'],
        'owner_members': owner_members,
        'all_members': all_members
    }

    return details


def channel_messages(token, channel_id, start):
    '''
    Implementing invite function by appending user to channel['all_members']
    '''

    if None in {token, channel_id, start}:
        raise InputError(description='Insufficient parameters')

    channel_id = int(channel_id)
    start = int(start)

    token_data = decode_token(token)
    channel = helpers.get_channel(channel_id)

    if start > len(channel['messages']):
        raise InputError(description='start is greater than end')

    # input error if channel doesn't exist.
    if helpers.get_channel(channel_id) is None:
        raise InputError(description='Channel does not exist.')

    # access error when authorized user not a member of channel.
    if helpers.is_channel_member(token_data['u_id'], channel_id) is False:
        raise AccessError(
            description='authorized user not a member of channel.')

    messages = {'messages': [], 'start': start, 'end': start + 50}

    for i in range(51):
        try:
            message = channel['messages'][start + i]
        except IndexError:
            messages['end'] = -1
            break

        message_reacts = []
        reacts = message['reacts']
        for react in reacts:
            is_this_user_reacted = token_data['u_id'] in react['u_ids']
            react_info = {
                'react_id': react['react_id'],
                'u_ids': react['u_ids'],
                'is_this_user_reacted': is_this_user_reacted
            }
            message_reacts.append(react_info)

        message_info = {
            'message_id': message['message_id'],
            'u_id': message['u_id'],
            'message': message['message'],
            'time_created': message['time_created'],
            'reacts': message_reacts,
            'is_pinned': message['is_pinned']
        }
        messages['messages'].append(message_info)

    return messages


def channel_leave(token, channel_id):
    '''
    Implementing leave function by removing user from channel['all_members']
    and channel['owner_members']
    '''

    if None in {token, channel_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    channel = helpers.get_channel(channel_id)

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # access error when authorized user not a member of channel.
    if helpers.is_channel_member(token_data['u_id'], channel_id) is False:
        raise AccessError(
            description='authorized user not a member of channel.')

    channel['all_members'].remove(token_data['u_id'])

    if helpers.is_user_admin(token_data['u_id'], channel_id):
        channel['owner_members'].remove(token_data['u_id'])

    return {}


def channel_join(token, channel_id):
    '''
    Implementing join function by appending user to channel['all_members']
    '''

    if None in {token, channel_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    channel = helpers.get_channel(channel_id)

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # access error when channel is private.
    if channel['is_public'] is False:
        raise AccessError(description='Channel is private.')

    # appends to channel['all_members'] if user not already a member.
    if helpers.is_channel_member(token_data['u_id'], channel_id) is False:
        helpers.channel_join(channel_id, token_data['u_id'])

    return {}


def channel_addowner(token, channel_id, u_id):
    '''
    Implementing addowner function by appending user to channel['owner_members']
    '''

    if None in {token, channel_id, u_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    channel = helpers.get_channel(channel_id)
    auth_user = token_data['token']

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # input error when user does not exist.
    if helpers.get_user(u_id) is None:
        raise InputError(description='User does not exist.')

    # input error if user already an owner of channel.
    if helpers.is_user_admin(u_id, channel_id) is True:
        raise InputError(description='User already owner of channel.')

    # access error when authorized user not owner of channel.
    if helpers.is_user_admin(auth_user, channel_id) is False:
        raise AccessError(description='Authorized user not owner of channel.')

    # appending user to owner members.
    if helpers.is_channel_member(u_id, channel_id) is False:
        channel['all_members'].append(u_id)

    channel['owner_members'].append(u_id)

    return {}


def channel_removeowner(token, channel_id, u_id):
    '''
    Implementing addowner function by appending user to channel['owner_members']
    '''
    if None in {token, channel_id, u_id}:
        raise InputError(description='Insufficient parameters')

    token_data = decode_token(token)
    channel = helpers.get_channel(channel_id)
    auth_user = token_data['u_id']

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # input error when user does not exist.
    if helpers.get_user(u_id) is None:
        raise InputError(description='User does not exist.')

    # input error when user is not an owner
    if helpers.is_user_admin(u_id, channel_id) is False:
        raise InputError(description='User is not an owner of channel.')

    # access error when authorized user not owner of channel.
    if helpers.is_user_admin(auth_user, channel_id) is False:
        raise AccessError(description='Authorized user not owner of channel.')

    # removing user from channel['owner_members']
    channel['owner_members'].remove(u_id)

    return {}
