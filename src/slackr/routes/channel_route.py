from json import dumps

from flask import Blueprint, request

from slackr.controllers import channel
from slackr.middleware import auth_middleware

CHANNEL_ROUTE = Blueprint('channel', __name__)


@CHANNEL_ROUTE.route("/channel/invite", methods=['POST'])
@auth_middleware
def route_channel_invite():
    '''Flask route for /channel/invite'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    return dumps(channel.channel_invite(token, channel_id, u_id))


@CHANNEL_ROUTE.route("/channel/details", methods=['GET'])
@auth_middleware
def route_channel_details():
    '''Flask route for /channel/details'''
    token = request.values.get('token')
    channel_id = request.values.get('channel_id')
    return dumps(channel.channel_details(token, channel_id))


@CHANNEL_ROUTE.route("/channel/messages", methods=['GET'])
@auth_middleware
def route_channel_messages():
    '''Flask route for /channel/messages'''
    token = request.values.get('token')
    channel_id = request.values.get('channel_id')
    start = request.values.get('start')
    return dumps(channel.channel_messages(token, channel_id, start))


@CHANNEL_ROUTE.route("/channel/leave", methods=['POST'])
@auth_middleware
def route_channel_leave():
    '''Flask route for /channel/leave'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    return dumps(channel.channel_leave(token, channel_id))


@CHANNEL_ROUTE.route("/channel/join", methods=['POST'])
@auth_middleware
def route_channel_join():
    '''Flask route for /channel/join'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    return dumps(channel.channel_join(token, channel_id))


@CHANNEL_ROUTE.route("/channel/addowner", methods=['POST'])
@auth_middleware
def route_channel_addowner():
    '''Flask route for /channel/addowner'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    return dumps(channel.channel_addowner(token, channel_id, u_id))


@CHANNEL_ROUTE.route("/channel/removeowner", methods=['POST'])
@auth_middleware
def route_channel_removeowner():
    '''Flask route for /channel/removeowner'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    return dumps(channel.channel_removeowner(token, channel_id, u_id))
