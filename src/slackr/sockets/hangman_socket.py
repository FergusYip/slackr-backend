from flask_socketio import emit
from slackr import socketio

from slackr.controllers import hangman


@socketio.on('hangman_start')
def socket_hangman_start(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    response = hangman.start_hangman(token, channel_id)
    emit('message_received', response, room=str(channel_id))


@socketio.on('hangman_guess')
def socket_hangman_guess(payload):
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    guess = payload.get('guess')
    response = hangman.guess_hangman(token, channel_id, guess)
    emit('message_received', response, room=str(channel_id))
