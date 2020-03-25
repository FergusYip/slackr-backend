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

    pass


@STANDUP.route("/standup/active", methods=['GET'])
def route_standup_active():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']


@STANDUP.route("/standup/send", methods=['POST'])
def route_standup_send():
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    pass
