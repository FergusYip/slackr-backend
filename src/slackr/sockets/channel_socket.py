from flask_socketio import emit
from slackr import socketio

from slackr.controllers import channels, channel


@socketio.on('channel_create')
def socket_channels_create(payload):
    token = payload.get('token')
    name = payload.get('name')
    is_public = payload.get('is_public')
    response = channels.channels_create(token, name, is_public)
    emit('channel_created', response, broadcast=True, include_self=False)
    emit('channel_joined', response)


@socketio.on('channel_join')
def socket_channels_create(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    response = channel.channel_join(token, channel_id)
    emit('channel_joined', response)


@socketio.on('channel_leave')
def socket_channels_create(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    response = channel.channel_leave(token, channel_id)
    emit('channel_left', response)
