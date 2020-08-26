from flask_socketio import emit
from slackr import socketio

from slackr.controllers import channels


@socketio.on('channel_create')
def socket_channels_create(payload):
    token = payload.get('token')
    name = payload.get('name')
    is_public = payload.get('is_public')
    response = channels.channels_create(token, name, is_public)
    print('channel_create')
    print(response)
    emit('channel_created', response, broadcast=True, include_self=False)
    emit('channel_joined', response)
