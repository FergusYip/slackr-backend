'''
Implementation of hangman game in a channel.
'''

import random
import wikiquote
from data_store import DATA_STORE as data_store
import helpers
from token_validation import decode_token
from error import InputError
import message
import token_validation


def start_hangman(token, channel_id):
    '''
    Initializes the hangman game.
    '''

    bot_token = token_validation.encode_token(-95)
    data_store['hangman_bot']['token'] = bot_token

    channel = helpers.get_channel(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    # setting hangman is_active to true.
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['hangman']['is_active'] = True
            channel['hangman']['word'] = get_line().lower()
            dashes = '_' * len(channel['hangman']['word'])

    message.message_send(bot_token, channel_id, dashes)


def guess_hangman(token, channel_id, guess):
    '''
    Main logic for hangman game.
    '''

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

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:

            # checking if hangman is_active is true.
            if channel['hangman']['is_active'] is False:
                raise InputError(description='game not active')

            # appending to list of guesses.
            channel['hangman']['guesses'].append(guess)

            # printing dashes.
            dashed = get_dashed(channel['hangman']['word'],
                                channel['hangman']['guesses'])
            message.message_send(token, channel_id, dashed)

            # incorrect guess.
            if guess not in channel['hangman']['word']:
                # printing the stage of game.
                wrong_guesses = len(channel['hangman']['guesses']) - \
                    len(channel['hangman']['correct'])
                message.message_send(token, channel_id, stages[wrong_guesses])

            # if more than 10 incorrect guesses.
            elif wrong_guesses > 10:
                message.message_send(token, channel_id, 'Game Over')
                channel['hangman']['is_active'] = False

            # correct guess.
            else:
                channel['hangman']['correct'].append(guess)

    # full word is guessed.
    if '_' not in dashed and len(channel['hangman']['guesses']) <= 10:
        message.message_send(token, channel_id, dashed)
        message.message_send(token, channel_id, 'Congratulations!')

    return {}


def get_dashed(word, guesses):
    '''
    Returns a string where all unguessed letters are '_'.
    '''

    # getting list of all lowercase letters.
    dashed = word
    for char in dashed:
        if char.lower() not in guesses and char.isalpha():
            dashed = dashed.replace(char, '_')
    return dashed


def get_quote():
    '''
    Function to get a random word from wikiquote
    '''
    word = random.choice(wikiquote.random_titles(lang='en'))
    brackets = {'{', '[', '(', '<'}
    for char in brackets:
        index = word.find(char)
        if index != -1:
            word = word[:index]
    word = word.strip()
    return word
