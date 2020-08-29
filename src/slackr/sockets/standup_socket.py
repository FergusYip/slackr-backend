from flask_socketio import emit
from slackr import socketio

from slackr.controllers import standup


def standup_end_callback(channel_id, message_details):
    socketio.emit('message_received', message_details, room=str(channel_id))


@socketio.on('standup_start')
def socket_standup_start(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    length = payload.get('length')
    response = standup.standup_start(token, channel_id, length,
                                     standup_end_callback)
    emit('standup_started', response, room=str(channel_id))
