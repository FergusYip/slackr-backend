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
import string


def start_hangman(token, channel_id):
    '''
    Initializes the hangman game.
    '''
    decode_token(token)
    bot_token = token_validation.encode_token(-95)
    data_store['hangman_bot']['token'] = bot_token

    # getting channel.
    channel_id = int(channel_id)
    channel = helpers.get_channel(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    if channel['hangman']['is_active'] is True:
        raise InputError(description='Game already in progress.')

    # initializing the game.
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['hangman']['is_active'] = True
            channel['hangman']['word'] = get_quote()
            dashes = get_dashed(channel['hangman']['word'],
                                channel['hangman']['guesses'])

            # sending the welcome message.
            welcome = f"Welcome to Hangman!\nWord:\t{dashes}"
            message.message_send(bot_token, channel_id, welcome)

    return {}


def guess_hangman(token, channel_id, guess):
    '''
    Main logic for hangman guesses.
    '''

    decode_token(token)
    channel_id = int(channel_id)
    channel = helpers.get_channel(channel_id)
    bot_token = data_store['hangman_bot']['token']
    dashed = 'hello'

    stages = {
        0: '',
        1: '=========',
        2: '|\n|\n|\n|\n=========',
        3: '+----------\n|\n|\n|\n|\n=========',
        4: '+----------\n|\t|\n|\n|\n|\n=========',
        5: '+----------\n|\t|\n|\tO\n|\n|\n=========',
        6: '+----------\n|\t|\n|\tO\n|      |\n|\n=========',
        7: '+----------\n|\t|\n|\tO\n|     /|\n|\n=========',
        8: '+----------\n|\t|\n|\tO\n|     /|\\\n|\n=========',
        9: '+----------\n|\t|\n|\tO\n|     /|\\\n|     /\n=========',
        10: '+----------\n|\t|\n|\tO\n|     /|\\\n|     /\\\n=========',
    }

    if channel is None:
        raise InputError(description='Channel does not exist.')

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:

            # checking if game is already active.
            if channel['hangman']['is_active'] is False:
                raise InputError(description='game not active')

            # appending to list of guesses.
            channel['hangman']['guesses'].append(guess.lower())

            # printing dashes.
            dashed = get_dashed(channel['hangman']['word'],
                                channel['hangman']['guesses'])

            wrong_guesses = [char for char in channel['hangman']
                             ['guesses'] if char not in channel['hangman']['correct']]

            # if more than 10 incorrect guesses.
            if len(wrong_guesses) >= 10:
                mess = f"Game Over.\nThe word was:\t{channel['hangman']['word']}"
                message.message_send(bot_token, channel_id, mess)

                # reset game.
                reset_hangman(channel_id)

            else:
                message.message_send(bot_token, channel_id, dashed)
                # incorrect guess.
                if guess.lower() not in channel['hangman']['word'].lower():
                    # printing the stage of game.
                    stage_mess = f"{stages[len(wrong_guesses)]}\nYou have guessed:\t{', '.join(wrong_guesses)}"
                    message.message_send(bot_token, channel_id, stage_mess)

                # correct guess.
                else:
                    channel['hangman']['correct'].append(guess)

    # full word is guessed.
    if '_' not in dashed:
        message.message_send(bot_token, channel_id,
                             'Congratulations! You win!')
        reset_hangman(channel_id)
    return {}


def get_dashed(word, guesses):
    '''
    Returns a string where all unguessed letters are '_'.
    '''

    # getting list of all lowercase letters.
    dashed = word
    for char in dashed:
        if char.lower() not in guesses and char.isalpha():
            dashed = dashed.replace(char, '_ ')
        elif char == ' ':
            dashed = dashed.replace(char, '   ')
    return dashed


def get_quote():
    '''
    Function to get a random word from wikiquote
    '''
    word = random.choice(wikiquote.random_titles(lang='en'))
    while not word.isalpha() and not check_ascii(word):
        word = random.choice(wikiquote.random_titles(lang='en'))
    return word


def check_ascii(word):
    '''
    Function to check if word is valid.
    '''
    for char in word:
        if char not in string.ascii_letters:
            return False

    return True


def reset_hangman(channel_id):
    '''
    Function to reset the hangman game.
    '''

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['hangman']['is_active'] = False
            channel['hangman']['word'] = None
            channel['hangman']['guesses'] = []
            channel['hangman']['correct'] = []
            channel['hangman']['stage'] = 0
