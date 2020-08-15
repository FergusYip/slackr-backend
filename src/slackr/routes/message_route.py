from json import dumps

from flask import Blueprint, request

from slackr.controllers import message as msg
from slackr.middleware import auth_middleware

MESSAGE_ROUTE = Blueprint('message', __name__)


@MESSAGE_ROUTE.route("/message/send", methods=['POST'])
@auth_middleware
def route_message_send():
    '''Flask route for /message/send'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    message = payload.get('message')
    return dumps(msg.message_send(token, channel_id, message))


@MESSAGE_ROUTE.route("/message/remove", methods=['DELETE'])
@auth_middleware
def route_message_remove():
    '''Flask route for /message/remove'''
    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    return dumps(msg.message_remove(token, message_id))


@MESSAGE_ROUTE.route("/message/edit", methods=['PUT'])
@auth_middleware
def route_message_edit():
    '''Flask route for /message/edit'''
    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    message = payload.get('message')
    return dumps(msg.message_edit(token, message_id, message))


@MESSAGE_ROUTE.route("/message/sendlater", methods=['POST'])
@auth_middleware
def route_message_sendlater():
    '''Flask route for /message/sendlater'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    message = payload.get('message')
    time_sent = payload.get('time_sent')
    return dumps(msg.message_sendlater(token, channel_id, message, time_sent))


@MESSAGE_ROUTE.route("/message/react", methods=['POST'])
@auth_middleware
def route_message_react():
    '''Flask route for /message/react'''
    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    react_id = payload.get('react_id')
    return dumps(msg.message_react(token, message_id, react_id))


@MESSAGE_ROUTE.route("/message/unreact", methods=['POST'])
@auth_middleware
def route_message_unreact():
    '''Flask route for /message/unreact'''
    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    react_id = payload.get('react_id')
    return dumps(msg.message_unreact(token, message_id, react_id))


@MESSAGE_ROUTE.route("/message/pin", methods=['POST'])
@auth_middleware
def route_message_pin():
    '''Flask route for /message/pin'''
    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    return dumps(msg.message_pin(token, message_id))


@MESSAGE_ROUTE.route("/message/unpin", methods=['POST'])
@auth_middleware
def route_message_unpin():
    '''Flask route for /message/unpin'''
    payload = request.get_json()
    token = payload.get('token')
    message_id = payload.get('message_id')
    return dumps(msg.message_unpin(token, message_id))
