from json import dumps
import threading
from flask import request, Blueprint
from token_validation import decode_token
from error import AccessError, InputError
from data_store import data_store
import helpers
from error import AccessError, InputError
from datetime import datetime, timezone
from data_store import data_store

STANDUP = Blueprint('standup', __name__)


@STANDUP.route("/standup/start", methods=['POST'])
def route_standup_start():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    length = payload['length']
    return dumps(standup_start(token, channel_id, length))


@STANDUP.route("/standup/active", methods=['GET'])
def route_standup_active():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    return dumps(standup_active(token, channel_id))


@STANDUP.route("/standup/send", methods=['POST'])
def route_standup_send():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    return dumps(standup_send(token, channel_id, message))


def standup_start(token, channel_id, length):
    '''
    Implementation of standup start function.
    '''
    decode_token(token)

    channel = helpers.get_channel(channel_id)
    if channel is None:
        raise InputError(description='Channel does not exist.')

    channel['standup']['is_active'] = True

    timer = threading.Timer(length, stop_standup(channel_id))
    timer.start()

    finish = int(datetime.now(timezone.utc).timestamp()) + length

    return finish


def stop_standup(channel_id):
    for channel in data_store['channels']:
        if channel['channel_id'] == channel_id:
            channel['standup']['is_active'] = False
            correct_channel = channel

    joined_message = ''

    # for every message dictionary in messages[]
    for message in correct_channel['standup']['messages']:
        joined_message += f"{message['handle_str']}: {message['message']}\n"


def standup_active(token, channel_id):
    # input error if channel does not exist.
    channel = helpers.get_channel(channel_id)
    if channel is None:
        raise InputError(description='Channel does not exist.')


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
            description='An active standup is not currently running in this channel')

    if u_id not in channel['all_members']:
        raise AccessError(
            description='The authorised user is not a member of the channel that the message is within'
        )

    message_dict = {'handle_str': helpers.get_handle(u_id), 'message': message}

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['standup']['messages'].append(message_dict)

    return {}
