from data_store import DATA_STORE as data_store
import helpers
from token_validation import decode_token
from error import AccessError, InputError`
import PyLyrics
import random
import message
import token_validation


def start_hangman(token, channel_id):
    bot_token = token_validation.encode_token(-95)
    data_store['hangman_bot']['token'] = bot_token

    channel = helpers.get_channel(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    # setting hangman is_active to true.
    for ch in data_store['channels']:
        if channel_id == ch['channel_id']:
            ch['hangman']['is_active'] = True
            ch['hangman']['word'] = getLine()

    dashes = '_' * len(ch['hangman']['word'])

    message.message_send(bot_token, channel_id, dashes)


def guess_hangman(token, channel_id, guess):
    decode_token(token)
    channel = helpers.get_channel(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    # setting hangman is_active to true.
    for ch in data_store['channels']:
        if channel_id == ch['channel_id']:
            if ch['hangman']['is_active'] is False:
                raise InputError(description='game not active')
            ch['hangman']['word'] = getLine()


def getLine():
    '''
    Function to get random line with PyLyrics
    '''

    lyrics = PyLyrics.getLyrics(
        'Rick Astley', 'Never Gonna Give You Up'))

    lyrics=lyrics.split('\n')

    filtered=[line for line in lyrics if len(line) > 5]

    return random.choice(filtered)
