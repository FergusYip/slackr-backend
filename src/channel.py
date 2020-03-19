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

channel = Blueprint('channel', __name__)


@channel.route("/invite", methods=['POST'])
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


@channel.route("/details", methods=['GET'])
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
    if helpers.is_user_in_channel(auth_user, c_id) is False:
        raise AccessError(description='Authorized user not in the channel')

    # finding the right channel.
    for ch in data_store['channels']:
        if ch['channel_id'] == c_id:
            channel = ch

    details = {
        'name': channel['name'],
        'owner_members': channel['owner_members'],
        'all_members': channel['all_members']
    }

    return dumps({details})


@channel.route("/messages", methods=['GET'])
def channel_messages(token, channel_id):
    payload = request.get_json()

    token = payload['token']
    token_data = decode_token(token)
    c_id = payload['channel_id']
    start = payload['start']
    channel = helpers.get_channel(c_id)

    message = {'messages': []}
    message['start'] = start

    # input error when the given start is greater than the id of last message.
    if start > len(channel['messages']):
        raise InputError(description='start is greater than end')

    # if channel doesn't exist.
    if helpers.get_channel(c_id) is None:
        raise InputError(description='Channel does not exist.')

    # access error when authorized user not a member of channel.
    if helpers.is_user_in_channel(token_data['u_id'], c_id) is False:
        raise AccessError(
            description='authorized user not a member of channel.')

    for i in range(51):
        mes = channel['messages'][start + i]

        # end of messages list
        if mes == channel['messages'][-1]:
            message['end'] = -1

        # reached start + 50
        elif mes == channel['messages'][start + 50]:
            message['end'] = start + 50
            message['messages'].append(mes)
            return dumps({message})

        message['messages'].append(mes)

    return dumps({message})


def channel_leave(token, channel_id):
    return {
    }


def channel_join(token, channel_id):
    return {
    }


def channel_addowner(token, channel_id, u_id):
    return {
    }


def channel_removeowner(token, channel_id, u_id):
    return {
    }
