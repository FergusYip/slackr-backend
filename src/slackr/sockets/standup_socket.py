from flask_socketio import emit
from slackr import socketio

from slackr.controllers import standup


@socketio.on('standup_start')
def socket_standup_start(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    length = payload.get('length')
    response = standup.standup_start(token, channel_id, length)
    emit('standup_started', response, room=str(channel_id))
