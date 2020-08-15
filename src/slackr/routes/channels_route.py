from json import dumps

from flask import Blueprint, request

from slackr.controllers import channels
from slackr.middleware import auth_middleware

CHANNELS_ROUTE = Blueprint('channels', __name__)


@CHANNELS_ROUTE.route("/channels/list", methods=['GET'])
@auth_middleware
def route_channels_list():
    '''Flask route for /channels/list'''
    token = request.values.get('token')
    return dumps(channels.channels_list(token))


@CHANNELS_ROUTE.route("/channels/listall", methods=['GET'])
@auth_middleware
def route_channels_listall():
    '''Flask route for /channels/listall'''
    token = request.values.get('token')
    return dumps(channels.channels_listall(token))


@CHANNELS_ROUTE.route("/channels/create", methods=['POST'])
@auth_middleware
def route_channels_create():
    '''Flask route for /channels/create'''
    payload = request.get_json()
    token = payload.get('token')
    name = payload.get('name')
    is_public = payload.get('is_public')
    return dumps(channels.channels_create(token, name, is_public))
