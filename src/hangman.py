'''
Functions to allow users to play a game of hangman in the program. Will allow
users to start a game in the channel and guess letters until they win/lose.
'''

import string
from data_store import DATA_STORE
from token_validation import encode_token, decode_token
from error import InputError
import message

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
    bot_token = encode_token(-95)
    DATA_STORE.preset_profiles['hangman_bot'].set_token(bot_token)

    # getting channel.
    channel_id = int(channel_id)
    channel = DATA_STORE.get_channel(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    if channel.hangman.is_active:
        raise InputError(description='Game already in progress.')

    word = channel.hangman.start()
    dashes = get_dashed(word, [])

    # sending the welcome message.
    welcome_msg = (f'Welcome to Hangman!\nWord:\t{dashes}')
    message.message_send(bot_token, channel_id, welcome_msg)

    return {}


def guess_hangman(token, channel_id, guess):
    '''
    Main logic for hangman guesses.
    '''

    decode_token(token)
    channel_id = int(channel_id)
    channel = DATA_STORE.get_channel(channel_id)
    bot_token = DATA_STORE.preset_profiles['hangman_bot'].token

    if channel is None:
        raise InputError(description='Channel does not exist.')

    # Check if game is already active.
    if channel.hangman.is_active is False:
        raise InputError(description='Game not active')

    # Check if there is a message to delete
    prev_msg_id = channel.hangman.prev_msg
    if None not in {prev_msg_id, DATA_STORE.get_message(prev_msg_id)}:
        message.message_remove(bot_token, channel.hangman.prev_msg)

    # Append guess to list of guesses.
    is_correct = channel.hangman.guess(guess)

    stage = channel.hangman.stage

    # Get dashed word
    dashed = get_dashed(channel.hangman.word, channel.hangman.guesses)

    if dashed == channel.hangman.word:
        win_msg = (f'Congratulations!\n'
                   f'You win!\n'
                   f'The word was {dashed}')
        message.message_send(bot_token, channel_id, win_msg)
        channel.hangman.stop()
    elif stage >= 10:
        lose = (f'Game Over.\n'
                f'{STAGES["stage"]}\n'
                f'The word was:  {channel.hangman.word}\n')
        prev = message.message_send(bot_token, channel_id, lose)
        channel.hangman.prev_msg = prev['message_id']

        # End and reset game.
        channel.hangman.stop()

    # incorrect guess.
    else:
        if is_correct is False:
            guess_result = 'Incorrect Guess.'
        else:
            guess_result = 'That was right!'

        wrong_guesses = channel.hangman.incorrect
        incorrect = (f'{guess_result}\n'
                     f'{STAGES["stage"]}\n'
                     f'{dashed}\n'
                     f'You have guessed:\t[ {", ".join(wrong_guesses)} ]\n')
        prev = message.message_send(bot_token, channel_id, incorrect)
        channel.hangman.prev_msg = prev['message_id']

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
