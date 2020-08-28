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
def socket_channel_join(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    response = channel.channel_join(token, channel_id)
    emit('channel_joined', response['channel'])
    emit('channel_new_member', response['user'], room=str(channel_id))


@socketio.on('channel_leave')
def socket_channel_leave(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    response = channel.channel_leave(token, channel_id)
    emit('channel_left', response['channel'])
    emit('channel_removed_member', response['user'], room=str(channel_id))


@socketio.on('channel_invite')
def socket_channel_invite(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    response = channel.channel_invite(token, channel_id, u_id)
    emit('channel_new_member', response['user'], room=str(channel_id))
    # Will have to find a way to emit only to invited user


@socketio.on('channel_addowner')
def socket_channel_addowner(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    response = channel.channel_addowner(token, channel_id, u_id)
    emit('channel_new_owner',
         response,
         room=str(channel_id),
         include_self=False)


@socketio.on('channel_removeowner')
def socket_channel_removeowner(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    u_id = payload.get('u_id')
    response = channel.channel_removeowner(token, channel_id, u_id)
    emit('channel_removed_owner',
         response,
         room=str(channel_id),
         include_self=False)


@socketio.on('channel_delete')
def socket_channels_remove(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    response = channels.channels_delete(token, channel_id)
    emit('channel_removed', response, broadcast=True, include_self=False)
