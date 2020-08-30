from flask_socketio import emit
from slackr import socketio
from slackr.controllers import message as msg


@socketio.on('message_send')
def handle_message_send(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    message = payload.get('message')
    emit('message_received',
         msg.message_send(token, channel_id, message),
         room=channel_id)


@socketio.on('message_remove')
def handle_message_remove(payload):
    '''Flask route for /message/remove'''
    token = payload.get('token')
    message_id = payload.get('message_id')

    message = msg.message_remove(token, message_id)
    channel_id = str(message['channel_id'])
    emit('message_removed', message, room=channel_id)


@socketio.on('message_edit')
def handle_message_edit(payload):
    token = payload.get('token')
    message_id = payload.get('message_id')
    message = payload.get('message')

    edited_message = msg.message_edit(token, message_id, message)
    channel_id = str(edited_message['channel_id'])
    emit('message_edited', edited_message, room=channel_id)


# @MESSAGE_ROUTE.route("/message/react", methods=['POST'])
# @auth_middleware
# @socketio.on('message_react')
# def socket_message_react(payload):
#     token = payload.get('token')
#     message_id = payload.get('message_id')
#     react_id = payload.get('react_id')
#     result = msg.message_react(token, message_id, react_id)
#     channel_id = str(result['channel_id'])
#     emit('message_reacted', result, room=channel_id)

# @MESSAGE_ROUTE.route("/message/unreact", methods=['POST'])
# @auth_middleware
# @socketio.on('message_unreact')
# def route_message_unreact(payload):
#     token = payload.get('token')
#     message_id = payload.get('message_id')
#     react_id = payload.get('react_id')
#     result = msg.message_unreact(token, message_id, react_id)
#     channel_id = str(result['channel_id'])
#     emit('message_unreacted', result, room=channel_id)


# @MESSAGE_ROUTE.route("/message/pin", methods=['POST'])
# @auth_middleware
@socketio.on('message_pin')
def socket_message_pin(payload):
    token = payload.get('token')
    message_id = payload.get('message_id')
    result = msg.message_pin(token, message_id)
    channel_id = str(result['channel_id'])
    emit('message_pinned', result, room=channel_id, include_self=False)


# @MESSAGE_ROUTE.route("/message/unpin", methods=['POST'])
# @auth_middleware
@socketio.on('message_unpin')
def socket_message_unpin(payload):
    token = payload.get('token')
    message_id = payload.get('message_id')
    result = msg.message_unpin(token, message_id)
    channel_id = str(result['channel_id'])
    emit('message_unpinned', result, room=channel_id, include_self=False)
