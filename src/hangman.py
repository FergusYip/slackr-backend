from string import ascii_lowercase
from data_store import DATA_STORE as data_store
import helpers
from token_validation import decode_token
from error import AccessError, InputError
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
            ch['hangman']['word'] = getLine().lower()

    dashes = '_' * len(ch['hangman']['word'])

    message.message_send(bot_token, channel_id, dashes)


def guess_hangman(token, channel_id, guess):
    decode_token(token)
    channel = helpers.get_channel(channel_id)

    stages = {
        0: '',
        1: '=========',
        2: '|\n|\n|\n|\n=========',
        3: '+----------\n|\n|\n|\n|\n=========',
        4: '+----------\n|    |\n|\n|\n|\n=========',
        5: '+----------\n|    |\n|    O\n|\n|\n=========',
        6: '+----------\n|    |\n|    O\n|    |\n|\n=========',
        7: '+----------\n|    |\n|    O\n|   /|\n|\n=========',
        8: '+----------\n|    |\n|    O\n|   /|\\\n|\n=========',
        9: '+----------\n|    |\n|    O\n|   /|\\\n|   /\n=========',
        10: '+----------\n|    |\n|    O\n|   /|\\\n|   /\\\n=========',
    }

    if channel is None:
        raise InputError(description='Channel does not exist.')

    for ch in data_store['channels']:
        if channel_id == ch['channel_id']:

            # checking if hangman is_active is true.
            if ch['hangman']['is_active'] is False:
                raise InputError(description='game not active')

            # appending to list of guesses.
            ch['hangman']['guesses'].append(guess)

            # if more than 10 guesses.
            if len(ch['hangman']['guesses']) > 10:
                message.message_send(token, channel_id, 'Game Over')
                ch['hangman']['is_active'] = False

            # incorrect guess.
            elif guess not in ch['hangman']['word']:
                # printing the stage of game.
                wrongGuesses = len(ch['hangman']['guesses']) - \
                    len(ch['hangman']['correct'])
                message.message_send(
                    token, channel_id, stages[wrongGuesses])

                # printing the dashes.
                message.message_send(
                    token, channel_id, getDashed(ch['hangman']['word'], ch['hangman']['guesses']))

            # correct guess.
            else:
                ch['hangman']['correct'].append(guess)

                # printing the dashes.
                message.message_send(
                    token, channel_id, getDashed(ch['hangman']['word'], ch['hangman']['guesses']))

    # full word is guessed.
    if '_' not in dashed and len(channel['hangman']['guesses']) <= 10:
        message.message_send(token, channel_id, dashed)
        message.message_send(token, channel_id, 'Congratulations!')
        return

    message.message_send(token, channel_id, stages[stage_var])


def getDashed(word, guesses):
    lowercase = [char for char in ascii_lowercase]
    dashed = word
    for char in lowercase:
        if char not in guesses:
            dashed = dashed.replace(char, '_')
    return dashed


def getLine():
    '''
    Function to get random line with PyLyrics
    '''

    lyrics = PyLyrics.getLyrics('Rick Astley', 'Never Gonna Give You Up')

    lyrics = lyrics.split('\n')

    filtered = [line for line in lyrics if len(line) > 5]

    return random.choice(filtered)
