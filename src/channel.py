import sys
import jwt
from json import dumps
from flask import Flask, request, Blueprint
from flask_cors import CORS
from error import AccessError, InputError
from data_store import data_store, SECRET
from token_validation import decode_token
import helpers

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

Channel = Blueprint('channel', __name__)


@Channel.route("/invite", methods=['POST'])
def channel_invite():
    payload = request.get_json()

    token = payload['token']
    c_id = payload['channel_id']
    invited = payload['u_id']

    token_data = decode_token(token)

    if helpers.get_user(invited) is None:
        raise InputError(description='User does not exist.')

    add_into_channel(token_data['u_id'], c_id, invited)

    return dumps({})


def add_into_channel(inviter, c_id, invited):
    '''
    Appends a user ID into the channel with ID c_id.
    '''
    for channel in data_store['channels']:
        if channel['channel_id'] == c_id:
            if inviter not in channel['all_members']:
                raise AccessError(
                    description='User does not have permission to invite')
            else:
                channel['all_members'].append(invited)


@Channel.route("/details", methods=['GET'])
def channel_details():
    payload = request.get_json()

    token = payload['token']
    c_id = payload['channel_id']

    token_data = decode_token(token)

    auth_user = token_data['u_id']

    # if channel doesn't exist.
    if helpers.get_channel(c_id) is None:
        raise InputError(description='Channel does not exist.')

    # if user asking for details is not in the channel.
    if helpers.is_channel_member(auth_user, c_id) is False:
        raise AccessError(description='Authorized user not in the channel')

    # finding the right channel.
    channel = helpers.get_channel(c_id)

    details = {
        'name': channel['name'],
        'owner_members': channel['owner_members'],
        'all_members': channel['all_members']
    }

    return dumps({details})


@Channel.route("/messages", methods=['GET'])
def channel_messages():
    payload = request.get_json()

    token = payload['token']
    token_data = decode_token(token)

    c_id = payload['channel_id']
    start = payload['start']
    channel = helpers.get_channel(c_id)

    messages = {'messages': [], 'start': start, 'end': start + 50}

    # input error when the given start is greater than the id of last message.
    if start > len(channel['messages']):
        raise InputError(description='start is greater than end')

    # input error if channel doesn't exist.
    if helpers.get_channel(c_id) is None:
        raise InputError(description='Channel does not exist.')

    # access error when authorized user not a member of channel.
    if helpers.is_channel_member(token_data['u_id'], c_id) is False:
        raise AccessError(
            description='authorized user not a member of channel.')

    for i in range(51):
        try:
            message = channel['messages'][start + i]
        except IndexError:
            messages['end'] = -1
            break

        message_reacts = []
        reacts = message['reacts']
        for react in reacts:
            is_this_user_reacted = token_data['u_id'] in react['u_id']
            react_info = {
                'react_id': react['react_id'],
                'u_ids': react['u_id'],
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

    return dumps(messages)  # shouldn't it be return dumps({message_info})?


@Channel.route("/leave", methods=['POST'])
def channel_leave():
    payload = request.get_json()

    token = payload['token']
    token_data = decode_token(token)

    c_id = payload['channel_id']
    channel = helpers.get_channel(c_id)

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

     # access error when authorized user not a member of channel.
    if helpers.is_channel_member(token_data['u_id'], c_id) is False:
        raise AccessError(
            description='authorized user not a member of channel.')

    channel['all_members'].remove(token_data['u_id'])

    if helpers.is_user_admin(token_data['u_id'], c_id):
        channel['owner_members'].remove(token_data['u_id'])

    return dumps({})


@Channel.route("/join", methods=['POST'])
def channel_join():
    payload = request.get_json()

    token = payload['token']
    token_data = decode_token(token)

    c_id = payload['channel_id']
    channel = helpers.get_channel(c_id)
    user = token_data['u_id']

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # access error when channel is private.
    if channel['is_public'] is False:
        raise AccessError(description='Channel is private.')

    # appends to channel['all_members'] if user not already a member.
    if helpers.is_channel_member(user, c_id) is False:
        channel['all_members'].append(user)

    return dumps({})


@Channel.route("/addowner", methods=['POST'])
def channel_addowner():
    payload = request.get_json()

    token = payload['token']
    token_data = decode_token(token)

    c_id = payload['channel_id']
    channel = helpers.get_channel(c_id)
    user = payload['u_id']
    auth_user = token_data['u_id']

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # input error when user does not exist.
    if helpers.get_user(user) is None:
        raise InputError(description='User does not exist.')

    # input error if user already an owner of channel.
    if helpers.is_user_admin(user, c_id) is True:
        raise InputError(description='User already owner of channel.')

    # access error when authorized user not owner of channel.
    if helpers.is_user_admin(auth_user, c_id) is False:
        raise AccessError(description='Authorized user not owner of channel.')

    # appending user to owner members.
    if helpers.is_channel_member(user, c_id) is False:
        channel['all_members'].append(user)

    channel['owner_members'].append(user)

    return dumps({})


@Channel.route('/removeowner', methods=['POST'])
def channel_removeowner():
    payload = request.get_json()

    token = payload['token']
    token_data = decode_token(token)

    c_id = payload['channel_id']
    channel = helpers.get_channel(c_id)
    user = payload['u_id']
    auth_user = token_data['u_id']

    # input error if channel doesn't exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    # input error when user does not exist.
    if helpers.get_user(user) is None:
        raise InputError(description='User does not exist.')

    # input error when user is not an owner
    if helpers.is_user_admin(user, c_id) is False:
        raise InputError(description='User is not an owner of channel.')

    # access error when authorized user not owner of channel.
    if helpers.is_user_admin(auth_user, c_id) is False:
        raise AccessError(description='Authorized user not owner of channel.')

    # removing user from channel['owner_members']
    channel['owner_members'].remove(user)

    return dumps({})
