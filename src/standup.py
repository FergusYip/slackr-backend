'''
Implementation of standup routes for slackr app
'''
from datetime import datetime, timezone
import threading
from token_validation import decode_token
from error import AccessError, InputError
from data_store import data_store
import helpers
from message import message_send


def standup_start(token, channel_id, length):
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

    channel_id = int(channel_id)
    channel = helpers.get_channel(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    if channel['standup']['is_active'] is True:
        raise InputError(
            description='An active standup is currently running on this channel'
        )

    finish = int(datetime.now(timezone.utc).timestamp()) + length

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['standup']['is_active'] = True
            channel['standup']['starting_user'] = u_id
            channel['standup']['time_finish'] = finish
            break

    timer = threading.Timer(length, stop_standup, args=[token, channel_id])
    timer.start()

    return {'time_finish': finish}


def stop_standup(token, channel_id):
    ''' Stops a standup in a specified channel and sends a message containing
        all standup messages

	Parameters:
		token (str): JWT
		channel_id (int): ID of the specified channel

	'''
    channel_id = int(channel_id)
    channel = helpers.get_channel(channel_id)

    if channel is None:
        return  # Unable to raise error in thread

    joined_message = ''
    for message in channel['standup']['messages']:
        joined_message += f"{message['handle_str']}: {message['message']}\n"

    for channel in data_store['channels']:
        if channel['channel_id'] == channel_id:
            channel['standup']['is_active'] = False
            channel['standup']['starting_user'] = None
            channel['standup']['time_finish'] = None
            channel['standup']['messages'].clear()
            break
    if len(joined_message) > 0:
        message_send(token, channel_id, joined_message)


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
    channel = helpers.get_channel(channel_id)

    if channel is None:
        raise InputError(description='Channel does not exist.')

    return {
        'is_active': channel['standup']['is_active'],
        'time_finish': channel['standup']['time_finish']
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

    channel_id = int(channel_id)
    channel = helpers.get_channel(channel_id)

    if channel is None:
        raise InputError(description='Channel ID is not a valid channel')

    if len(message) > 1000:
        raise InputError(description='Message is more than 1000 characters')

    if len(message) == 0:
        raise InputError(description='Message cannot be zero characters')

    if channel['standup']['is_active'] is False:
        raise InputError(
            description=
            'An active standup is not currently running in this channel')

    if u_id not in channel['all_members']:
        raise AccessError(
            description=
            'The authorised user is not a member of the channel that the message is within'
        )

    message_dict = {'handle_str': helpers.get_handle(u_id), 'message': message}

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['standup']['messages'].append(message_dict)

    return {}
