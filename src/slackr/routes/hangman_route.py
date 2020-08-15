from json import dumps

from flask import Blueprint, request

from slackr.controllers import hangman
from slackr.middleware import auth_middleware

HANGMAN_ROUTE = Blueprint('hangman', __name__)


@HANGMAN_ROUTE.route("/hangman/start", methods=['POST'])
@auth_middleware
def route_hangman_start():
    '''Flask route for /hangman/start'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    return dumps(hangman.start_hangman(token, channel_id))


@HANGMAN_ROUTE.route("/hangman/guess", methods=['POST'])
@auth_middleware
def route_hangman_guess():
    '''Flask route for /hangman/start'''
    payload = request.get_json()
    token = payload.get('token')
    channel_id = payload.get('channel_id')
    guess = payload.get('guess')
    return dumps(hangman.guess_hangman(token, channel_id, guess))
