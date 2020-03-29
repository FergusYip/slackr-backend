from json import dumps
import threading
from flask import request, Blueprint
from token_validation import decode_token
from error import AccessError, InputError
from data_store import data_store
import helpers
from datetime import datetime, timezone
from message import message_send

STANDUP = Blueprint('standup', __name__)


@STANDUP.route("/standup/start", methods=['POST'])
def route_standup_start():
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    length = int(payload['length'])
    return dumps(standup_start(token, channel_id, length))


@STANDUP.route("/standup/active", methods=['GET'])
def route_standup_active():
    token = request.values.get('token')
    channel_id = int(request.values.get('channel_id'))
    return dumps(standup_active(token, channel_id))


@STANDUP.route("/standup/send", methods=['POST'])
def route_standup_send():
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']
    return dumps(standup_send(token, channel_id, message))


def standup_start(token, channel_id, length):
    '''
    Implementation of standup start function.
    '''
    token_info = decode_token(token)
    u_id = token_info['u_id']

    channel = helpers.get_channel(channel_id)

    # if channel is None:
    #     raise InputError(description='Channel does not exist.')

    if channel['standup']['is_active'] is True:
        raise InputError(
            description='An active standup is currently running on this channel'
        )

    finish = int(datetime.now(timezone.utc).timestamp()) + length

    for ch in data_store['channels']:
        if channel_id == ch['channel_id']:
            ch['standup']['is_active'] = True
            ch['standup']['starting_user'] = u_id
            ch['standup']['time_finish'] = finish
            break

    timer = threading.Timer(length, stop_standup, args=[token, channel_id])
    timer.start()

    return {'time_finish': finish}


def stop_standup(token, channel_id):

    ch = helpers.get_channel(channel_id)
    joined_message = ''

    # for every message dictionary in messages[]
    for message in ch['standup']['messages']:
        joined_message += f"{message['handle_str']}: {message['message']}\n"

    for channel in data_store['channels']:
        if channel['channel_id'] == channel_id:
            channel['standup']['is_active'] = False
            channel['standup']['starting_user'] = None
            channel['standup']['time_finish'] = None
            channel['standup']['messages'].clear()
            break
    if len(joined_message) > 0:
        message_send(token, channel_id, joined_message)


def standup_active(token, channel_id):
    decode_token(token)

    # input error if channel does not exist.
    channel = helpers.get_channel(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    return {
        'is_active': channel['standup']['is_active'],
        'time_finish': channel['standup']['time_finish']
    }


def standup_send(token, channel_id, message):
    token_info = decode_token(token)
    u_id = token_info['u_id']

    channel = helpers.get_channel(channel_id)

    if channel is None:
        raise InputError(description="Channel ID is not a valid channel")

    if len(message) > 1000:
        raise InputError(description='Message is more than 1000 characters')

    if channel['standup']['is_active'] is False:
        raise InputError(
            description=
            'An active standup is not currently running in this channel')

    if u_id not in channel['all_members']:
        raise AccessError(
            description=
            'The authorised user is not a member of the channel that the message is within'
        )

    message_dict = {'handle_str': helpers.get_handle(u_id), 'message': message}

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['standup']['messages'].append(message_dict)

    return {}
