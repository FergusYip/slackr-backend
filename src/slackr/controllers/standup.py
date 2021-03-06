'''
Functions to allow users participate in a standup in the program. Will allow
users to start a timed standup where messages sent before the end time will
be joined into one standup summary message.
'''
import threading

from slackr import helpers
from slackr.controllers.message import message_send
from slackr.error import AccessError, InputError
from slackr.models.channel import Channel
from slackr.models.user import User
from slackr.token_validation import decode_token
from slackr import db
from slackr.models.message import Message


def standup_start(token, channel_id, length, callback=None):
    ''' Starts a standup in a specified channel

	Parameters:
		token (str): JWT
		channel_id (int): ID of the specified channel
		length (int): Duration of the standup in seconds

	Returns (dict):
		time_finish (int): Unix timestamp of when the standup finishes

	'''

    if None in {token, channel_id, length}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = token_info['u_id']
    user = User.query.get(u_id)

    channel_id = int(channel_id)
    channel = Channel.query.get(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    if channel.standup.is_active is True:
        raise InputError(
            description='An active standup is currently running on this channel'
        )

    time_finish = helpers.utc_now() + length

    # channel.standup.start(user, time_finish)

    channel.standup.starting_user = user
    channel.standup.is_active = True
    channel.standup.time_finish = time_finish

    db.session.commit()

    timer = threading.Timer(length,
                            stop_standup,
                            args=[token, channel.channel_id, callback])
    timer.start()

    return {'standup_id': channel.standup.id, 'time_finish': time_finish}


def stop_standup(token, channel_id, callback=None):
    ''' Stops a standup in a specified channel and sends a message containing
        all standup messages

	Parameters:
		token (str): JWT
		channel_id (int): ID of the specified channel
    '''

    token_info = decode_token(token)
    u_id = token_info['u_id']
    user = User.query.get(u_id)

    channel = Channel.query.get(channel_id)

    channel.standup.is_active = False
    channel.standup.starting_user = None
    channel.standup.time_finish = None

    message = channel.standup.message
    channel.standup.message = ''

    db.session.commit()

    if message:
        prev_msg = message_send(token, channel_id, message)
        if callback:
            standup_message = Message.query.get(prev_msg['message_id'])
            callback(channel_id, standup_message.details(user))


def standup_active(token, channel_id):
    ''' Checks if a standup is active in a specified channel

	Parameters:
		token (str): JWT
		channel_id (int): ID of the specified channel

	Returns (dict):
		is_active (bool): Whether a standup is active in the channel
		time_finish (int): Unix timestamp of when the standup finishes
                           (if there is an active standup)

	'''

    if None in {token, channel_id}:
        raise InputError(description='Insufficient parameters')

    decode_token(token)

    channel_id = int(channel_id)
    channel = Channel.query.get(channel_id)

    # input error if channel does not exist.
    if channel is None:
        raise InputError(description='Channel does not exist.')

    return {
        'is_active': channel.standup.is_active,
        'time_finish': channel.standup.time_finish
    }


def standup_send(token, channel_id, message):
    ''' Send a standup message

	Parameters:
		token (str): JWT
		channel_id (int): ID of the specified channel
		message (str): Message

	Returns:
        (dict) : Empty dictionary

	'''

    if None in {token, channel_id, message}:
        raise InputError(description='Insufficient parameters')

    token_info = decode_token(token)
    u_id = token_info['u_id']
    user = User.query.get(u_id)

    channel_id = int(channel_id)
    channel = Channel.query.get(channel_id)

    if channel is None:
        raise InputError(description="Channel ID is not a valid channel")

    if len(message) > 1000:
        raise InputError(
            description='Message cannot be more than 1000 characters')

    if not message:
        raise InputError(description='Message cannot be zero characters')

    if channel.standup.is_active is False:
        raise InputError(
            description=
            'An active standup is not currently running in this channel')

    if user not in channel.all_members:
        raise AccessError(
            description=
            'The authorised user is not a member of the channel that the message is within'
        )

    channel.standup.message += f"{user.handle_str}: {message}\n"
    db.session.commit()

    return {}
