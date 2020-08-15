'''
Functions to allow users to play a game of hangman in the program. Will allow
users to start a game in the channel and guess letters until they win/lose.
'''

import slackr.controllers.message as message
from slackr.error import InputError
from slackr.models.channel import Channel
from slackr.models.message import Message
from slackr.token_validation import decode_token, encode_token
from slackr.utils.constants import RESERVED_UID

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

    dashes = channel.hangman.start()

    bot_token = encode_token(RESERVED_UID['hangman_bot'])

    # sending the welcome message.
    welcome_msg = (f'Welcome to Hangman!\nWord:\t{dashes}')
    prev = message.message_send(bot_token, channel_id, welcome_msg)
    channel.hangman.set_prev_msg_id(prev['message_id'])

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
    if None not in {prev_msg_id, Message.query.get(prev_msg_id)}:
        message.message_remove(bot_token, prev_msg_id)

    # Append guess to list of guesses.
    is_correct = channel.hangman.guess(guess)

    stage = channel.hangman.stage

    # Get dashed word
    dashed = channel.hangman.get_dashed()

    if dashed == channel.hangman.word:
        msg = (f'Congratulations!\n' f'You win!\n' f'The word was {dashed}')
        channel.hangman.stop()

    elif stage >= 10:
        msg = (f'Game Over.\n'
               f'{STAGES[stage]}\n'
               f'The word was:  {channel.hangman.word}\n')
        channel.hangman.stop()

    # incorrect guess.
    else:
        if is_correct is False:
            guess_result = 'Incorrect Guess.'
        else:
            guess_result = 'That was right!'

        msg = (
            f'{guess_result}\n'
            f'{STAGES[stage]}\n'
            f'{dashed}\n'
            f'You have guessed:\t[ {", ".join(channel.hangman.incorrect)} ]\n')

    prev = message.message_send(bot_token, channel_id, msg)
    channel.hangman.set_prev_msg_id(prev['message_id'])

    return {}
