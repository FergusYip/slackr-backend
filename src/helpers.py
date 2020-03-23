''' Helper module with functions to access values from data_store'''

from datetime import datetime, timezone
from data_store import data_store


def get_channel(channel_id):
    """ Returns channel with id channel_id

	Parameters:
		channel_id (int): The id of the channel

	Returns:
		channel (dict): Dictionary of channel details
		None : If no channel with channel_id exists

	"""
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            return channel
    return None


def get_message(message_id, channel_id):
    """ Returns message with id message_id

	Parameters:
		message_id (int): The id of the message
		channel_id (int): The id of the channel containing the message

	Returns:
		message (dict): Dictionary of message details
		None : If message was not found

	"""
    channel = get_channel(channel_id)
    for message in channel['messages']:
        if message_id == message['message_id']:
            return message
    return None


def message_existance(message_id, channel_id):
    """ Returns whether a message with message_id exists in channel with channel_id

	Parameters:
		message_id (int): The id of the message
		channel_id (int): The id of the channel containing the message

	Returns:
		(bool): Whether the message is in channel

	"""
    if get_message(message_id, channel_id) is not None:
        return True
    return False


def get_user(u_id):
    """ Returns a user with u_id

	Parameters:
		u_id (int): The id of the user

	Returns:
		user (dict): Dictionary of user details
		None : If user was not found

	"""
    for user in data_store['users']:
        if user['u_id'] == u_id:
            return user
    return None


def is_owner(u_id):
    """ Returns whether a user is a owner

	Parameters:
		u_id (int): The id of the user

	Returns:
		(bool) : Whether the user is a owner

	"""
    user = get_user(u_id)
    if user['permission_id'] == data_store['permissions']['owner']:
        return True
    return False


def is_user_admin(u_id, channel_id):
    """ Returns whether a user has admin permissions in a channel

	Parameters:
		u_id (int): The id of the user
		channel_id (int): The id of the channel

	Returns:
		(bool) : Whether the user has admin permissions in a channel

	"""
    user_info = get_user(u_id)
    if user_info is None:
        return False
    if user_info['permission_id'] == 1:
        return True
    channel_info = get_channel(channel_id)
    if channel_info is None:
        return False
    if u_id in channel_info['owner_members']:
        return True
    return False


def is_channel_member(user_id, channel_id):
    """ Returns whether a user is a member of the channel

	Parameters:
		u_id (int): The id of the user
		channel_id (int): The id of the channel

	Returns:
		(bool) : Whether the user is a member of the channel

	"""
    channel = get_channel(channel_id)
    if user_id in channel['all_members']:
        return True
    return False


def utc_now():
    """ Returns the current UTC time in Unix time

	Parameters:
		None

	Returns:
		(int) : Current UTC Time in Unix time

	"""
    return int(datetime.now(timezone.utc).timestamp())


def get_react(message_id, channel_id, react_id):
    """ Returns the react with id react_id

	Parameters:
		react_id (int): The id of the react
		message_id (int): The id of the message
		channel_id (int): The id of the channel containing the message

	Returns:
		react (dict) : Dictionary of react details
		None: If react doesn't exist

	"""
    message = get_message(message_id, channel_id)
    for react in message['reacts']:
        if react_id == react['react_id']:
            return react
    return None


def is_pinned(message_id, channel_id):
    """ Returns whether a message is pinned

	Parameters:
		message_id (int): The id of the message
		channel_id (int): The id of the channel containing the message

	Returns:
		(bool): Whether the message is pinned

	"""
    message = get_message(message_id, channel_id)
    return message['is_pinned']


def has_user_reacted(u_id, message_id, channel_id, react_id):
    """ Returns whether a user has reacted to a message using the react with id react_id

	Parameters:
		u_id (int): The id of the user
		message_id (int): The id of the message
		channel_id (int): The id of the channel containing the message
		react_id (int): The id of the react

	Returns:
		(bool): Whether the user has reacted to a message using the react with id react_id

	"""
    react = get_react(message_id, channel_id, react_id)
    if u_id in react['u_ids']:
        return True
    return False


def get_all_u_id():
    """ Returns u_ids of all users

	Parameters:
		None

	Returns:
		(list): List of all u_ids

	"""
    return [user['u_id'] for user in data_store['users']]


def get_permissions():
    """ Returns a list of valid permissions

	Parameters:
		None

	Returns:
		(list): List of valid permissions

	"""
    return data_store['permissions'].values()

def user_change_first_last_name(u_id, first_name, last_name):
    for user in data_store['users']:
        if user['u_id'] == u_id:
            user['name_first'] = first_name
            user['name_last'] = last_name
            break

def user_change_email(u_id, email):
    for user in data_store['users']:
        if user['u_id'] == u_id:
            user['email'] = email
            break

def user_check_name(name):
    if 1 <= len(name) <= 50:
        return True
    else: 
        return False

def is_email_used(email):
    for user in data_store['users']:
        if user['email'] == email:
            return True
    return False

def is_handle_used(handle):
    for user in data_store['users']:
        if user['handle_str'] == handle:
            return True
    return False

def handle_length_check(handle):
    if 2 <= len(handle) <= 20:
        return True
    else:
        return False

def user_change_handle(u_id, handle):
    for user in data_store['users']:
        if user['u_id'] == u_id:
            user['handle_str'] = handle
            break

if __name__ == '__main__':
    pass
