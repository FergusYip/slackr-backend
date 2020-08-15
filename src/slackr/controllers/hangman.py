'''
Functions to allow users to play a game of hangman in the program. Will allow
users to start a game in the channel and guess letters until they win/lose.
'''

import string

import slackr.controllers.message as message
from slackr import db, helpers
from slackr.error import InputError
from slackr.models.channel import Channel
from slackr.models.hangman import Hangman
from slackr.models.message import Message
from slackr.models.user import User
from slackr.token_validation import decode_token, encode_token
from slackr.utils.constants import RESERVED_UID, PERMISSIONS

# Game stages
STAGES = {
    0: '',
    1: '=========',
    2: '|\n|\n|\n|\n=========',
    3: '+------\n|\n|\n|\n|\n=========',
    4: '+------\n|\t|\n|\n|\n|\n=========',
    5: '+------\n|\t|\n|\tO\n|\n|\n=========',
    6: '+------\n|\t|\n|\tO\n|       |\n|\n=========',
    7: '+------\n|\t|\n|\tO\n|      /|\n|\n=========',
    8: '+------\n|\t|\n|\tO\n|      /|\\\n|\n=========',
    9: '+------\n|\t|\n|\tO\n|      /|\\\n|      /\n=========',
    10: '+------\n|\t|\n|\tO\n|      /|\\\n|      /\\\n=========',
}


def start_hangman(token, channel_id):
    '''
    Initializes the hangman game.
    '''
    decode_token(token)

    # getting channel.
    channel_id = int(channel_id)
    channel = Channel.query.get(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    if channel.hangman.is_active:
        raise InputError(description='Game already in progress.')

    word = helpers.get_word()

    channel.hangman.is_active = True
    channel.hangman.word = word

    db.session.commit()

    dashes = get_dashed(word, [])

    bot_token = encode_token(RESERVED_UID['hangman_bot'])

    # sending the welcome message.
    welcome_msg = (f'Welcome to Hangman!\nWord:\t{dashes}')
    prev = message.message_send(bot_token, channel_id, welcome_msg)
    channel.hangman.prev_msg_id = prev['message_id']
    db.session.commit()

    return {}


def guess_hangman(token, channel_id, guess):
    '''
    Main logic for hangman guesses.
    '''

    decode_token(token)
    channel_id = int(channel_id)
    channel = Channel.query.get(channel_id)
    bot_token = encode_token(RESERVED_UID['hangman_bot'])

    if channel is None:
        raise InputError(description='Channel does not exist.')

    # Check if game is already active.
    if channel.hangman.is_active is False:
        raise InputError(description='Game not active')

    # Check if there is a message to delete
    prev_msg_id = channel.hangman.prev_msg_id
    print(f'prev_msg is {prev_msg_id}')
    if None not in {prev_msg_id, Message.query.get(prev_msg_id)}:
        message.message_remove(bot_token, prev_msg_id)

    # Append guess to list of guesses.
    is_correct = guess_letter(channel.channel_id, guess)

    stage = channel.hangman.stage

    # Get dashed word
    dashed = get_dashed(channel.hangman.word, channel.hangman.guesses)

    if dashed == channel.hangman.word:
        win_msg = (f'Congratulations!\n'
                   f'You win!\n'
                   f'The word was {dashed}')
        message.message_send(bot_token, channel_id, win_msg)
        stop(channel_id)

    elif stage >= 10:
        lose = (f'Game Over.\n'
                f'{STAGES[stage]}\n'
                f'The word was:  {channel.hangman.word}\n')
        message.message_send(bot_token, channel_id, lose)

        # End and reset game.
        stop(channel_id)

    # incorrect guess.
    else:
        if is_correct is False:
            guess_result = 'Incorrect Guess.'
        else:
            guess_result = 'That was right!'

        wrong_guesses = [letter for letter in channel.hangman.incorrect]
        incorrect = (f'{guess_result}\n'
                     f'{STAGES[stage]}\n'
                     f'{dashed}\n'
                     f'You have guessed:\t[ {", ".join(wrong_guesses)} ]\n')
        prev = message.message_send(bot_token, channel_id, incorrect)
        channel.hangman.prev_msg_id = prev['message_id']
        db.session.commit()

    return {}


def get_dashed(word, guesses):
    '''
    Returns a string where all unguessed letters are '_'.
    '''
    for char in word:
        if char not in string.ascii_letters:
            return False

    # getting list of all lowercase letters.
    dashed = word
    for char in dashed:
        if char.lower() not in guesses and char.isalpha():
            dashed = dashed.replace(char, '_ ')
        elif char == ' ':
            dashed = dashed.replace(char, '   ')
    return dashed


def guess_letter(channel_id, letter):
    channel = Channel.query.get(channel_id)
    letter = letter.lower()
    if letter not in channel.hangman.guesses:
        channel.hangman.guesses += letter

    # incorrect guess
    is_correct = True
    if letter not in channel.hangman.word.lower():
        if letter not in channel.hangman.incorrect:
            channel.hangman.stage += 1
            channel.hangman.incorrect += letter
        is_correct = False

    db.session.commit()

    return is_correct


def stop(channel_id):
    channel = Channel.query.get(channel_id)
    channel.hangman.is_active = False
    channel.hangman.word = None
    channel.hangman.guesses = ''
    channel.hangman.incorrect = ''
    channel.hangman.stage = 0
    channel.hangman.prev_msg_id = 0
    db.session.commit()
