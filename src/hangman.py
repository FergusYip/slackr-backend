'''
Implementation of hangman game in a channel.
'''

from data_store import DATA_STORE
from token_validation import decode_token
from error import InputError
import message
import token_validation


def start_hangman(token, channel_id):
    '''
    Initializes the hangman game.
    '''
    decode_token(token)
    bot_token = token_validation.encode_token(-95)
    DATA_STORE.preset_profiles['hangman_bot'].token = bot_token

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
    welcome = f"Welcome to Hangman!\nWord:\t{dashes}"
    message.message_send(bot_token, channel_id, welcome)

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

    # checking if game is already active.
    if channel.hangman.is_active is False:
        raise InputError(description='Game not active')

    if channel.hangman.prev_msg is not None:
        print(channel.hangman.prev_msg)
        message.message_remove(bot_token, channel.hangman.prev_msg)

    # appending to list of guesses.
    is_correct = channel.hangman.guess(guess)

    stage = channel.hangman.stage

    # printing dashes.
    dashed = get_dashed(channel.hangman.word, channel.hangman.guesses)

    # if more than 10 incorrect guesses.
    if dashed == channel.hangman.word:
        message.message_send(bot_token, channel_id,
                             'Congratulations! You win!')
        channel.hangman.stop()
    elif stage > 10:
        lose = (f"Game Over.\n"
                f"{stages[stage]}\n"
                f"The word was:\t{channel['hangman']['word']}\n")
        prev = message.message_send(bot_token, channel_id, lose)
        channel.hangman.prev_msg = int(prev['message_id'])

        # End and reset game.
        channel.hangman.stop()

    # incorrect guess.
    elif is_correct is False:
        # printing the stage of game.
        wrong_guesses = channel.hangman.incorrect
        incorrect = (f"Incorrect Guess.\n"
                     f"{stages[stage]}\n"
                     f"{dashed}\n"
                     f"You have guessed:\t[ {', '.join(wrong_guesses)} ]\n")
        prev = message.message_send(bot_token, channel_id, incorrect)
        channel.hangman.prev = int(prev['message_id'])

    # Correct guess.
    else:
        correct = (f"That was right!\n" f"{dashed}\n")
        prev = message.message_send(bot_token, channel_id, correct)
        channel.hangman.prev = int(prev['message_id'])

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
