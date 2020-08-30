from json import dumps

from flask import Blueprint, request

from slackr.controllers import standup
from slackr.middleware import auth_middleware

STANDUP_ROUTE = Blueprint('standup', __name__)


@STANDUP_ROUTE.route("/standup/start", methods=['POST'])
@auth_middleware
def route_standup_start():
    '''Flask route for /standup/start'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    length = payload.get('length')
    return dumps(standup.standup_start(token, channel_id, length))


@STANDUP_ROUTE.route("/standup/active", methods=['GET'])
@auth_middleware
def route_standup_active():
    '''Flask route for /standup/active'''
    token = request.values.get('token')
    channel_id = request.values.get('channel_id')
    return dumps(standup.standup_active(token, channel_id))


@STANDUP_ROUTE.route("/standup/send", methods=['POST'])
@auth_middleware
def route_standup_send():
    '''Flask route for /standup/send'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    message = payload.get('message')
    return dumps(standup.standup_send(token, channel_id, message))


@STANDUP_ROUTE.route("/standup/fetch_previous", methods=['GET'])
@auth_middleware
def route_standup_fetch_previous():
    '''Flask route for /standup/active'''
    token = request.values.get('token')
    channel_id = request.values.get('channel_id')
    return dumps(standup.standup_fetch_previous(token, channel_id))
