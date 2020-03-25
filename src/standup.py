from json import dumps
from flask import request, Blueprint
from token_validation import decode_token
import helpers

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
    pass


def standup_active(token, channel_id):
    pass


def standup_send(token, channel_id, message):
    token_info = decode_token(token)
    u_id = token_info['u_id']

    message_dict = {'handle_str': helpers.get_handle(u_id), 'message': message}

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['standup']['messages'].append(message_dict)

    return {}
