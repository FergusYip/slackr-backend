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


def get_message(message_id):
    """ Returns message with id message_id

	Parameters:
		message_id (int): The id of the message

	Returns:
		message (dict): Dictionary of message details
		None : If message was not found

	"""
    for channel in data_store['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                return message
    return None


def get_user(u_id=None, email=None):
    """ Returns a user with u_id

	Parameters:
		u_id (int): The id of the user
        email (str): The email of the user

	Returns:
		user (dict): Dictionary of user details
		None : If user was not found

	"""
    for user in data_store['users']:
        if user['u_id'] == u_id or user['email'] == email:
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
    message = get_message(message_id)
    if message == None:
        return None
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
    message = get_message(message_id)
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
    if react is None:
        return False

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
    """ Checks whether a name is invalid

	Parameters:
		name (str): Name

	Returns:
		(bool): Whether the name is invalid

	"""
    if 1 <= len(name) <= 50:
        return True
    return False


def is_email_used(email):
    for user in data_store['users']:
        if user['email'] == email:
            return True
    return False


def is_handle_used(handle):
    """ Checks if a handle is unique

	Parameters:
		handle_str (str): User handle
	Returns:
		(bool): Whether the handle is used by another user
        
	"""
    for user in data_store['users']:
        if user['handle_str'] == handle:
            return True
    return False


def handle_length_check(handle):
    if 2 <= len(handle) <= 20:
        return True
    else:
        return False


def get_handle(u_id):
    for user in data_store['users']:
        if u_id == user['u_id']:
            return user['handle_str']
    return None


def user_change_handle(u_id, handle):
    for user in data_store['users']:
        if user['u_id'] == u_id:
            user['handle_str'] = handle
            break


def message_send_message(message_dict, channel_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['messages'].append(message_dict)
            break


def message_remove_message(message_dict, channel_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['messages'].remove(message_dict)
            break


def message_edit_message(new_message, message_id, channel_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    message['message'] = new_message
                    break


def message_add_react(react_dict, message_id, channel_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    message['reacts'].append(react_dict)
                    break


def message_add_react_uid(user_id, message_id, channel_id, react_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    for react in message['reacts']:
                        if react_id == react['react_id']:
                            react['u_ids'].append(user_id)
                            break


def message_remove_react_uid(user_id, message_id, channel_id, react_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    for react in message['reacts']:
                        if react_id == react['react_id']:
                            react['u_ids'].remove(user_id)
                            break


def message_remove_reaction(react_dict, message_id, channel_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    message['reacts'].remove(react_dict)
                    break


def message_pin(message_id, channel_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    message['is_pinned'] = True
                    break


def message_unpin(message_id, channel_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    message['is_pinned'] = False
                    break


def user_channels(u_id):
    '''Retrieve a list of a user's joined channels'''
    return [
        channel for channel in data_store['channels']
        if u_id in channel['all_members']
    ]


def channel_search(channel, query_str):
    '''Retrieve all messages in a channel which contain the query string'''
    return [
        message for message in channel['messages']
        if query_str in message['message']
    ]


def channel_join(channel_id, u_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['all_members'].append(u_id)


def generate_id(id_type):
    """ Generates ID of id_type

	Parameters:
		id_type (str): Type of ID to generate

	Returns:
		u_id (int): User ID

	"""
    data_store['max_ids'][id_type] += 1
    return data_store['max_ids'][id_type]


def generate_u_id():
    """ Generates u_id

	Returns:
		u_id (int): User ID

	"""
    data_store['max_ids']['u_id'] += 1
    return data_store['max_ids']['u_id']


def generate_message_id():
    '''
    Function that will generate a unique message_id within a specific channel.
    '''

    message_id = data_store['max_ids']['message_id'] + 1

    data_store['max_ids']['message_id'] = message_id

    return message_id


def get_channel_from_message(message_id):
    for channel in data_store['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                return channel
    return None


def get_channel_message(message_id):
    for channel in data_store['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                return {'channel': channel, 'message': message}
    return None


if __name__ == '__main__':
    pass
