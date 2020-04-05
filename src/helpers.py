''' Helper module with functions to access values from data_store'''

from datetime import datetime, timezone
from data_store import data_store


def get_channel(channel_id):
    """
    Returns channel with id channel_id.

	Parameters:
		channel_id (int): The id of the channel

	Returns:
		channel (dict): Dictionary of channel details
		None : If no channel with channel_id exists
	"""
    channel_id = int(channel_id)
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            return channel
    return None


def get_message(message_id):
    """
    Returns message with id message_id.

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
    """
    Returns a user with u_id.

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
    """
    Returns whether a user is a owner.

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
    """
    Returns whether a user has admin permissions in a channel.

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
    """
    Returns whether a user is a member of the channel.

	Parameters:
		u_id (int): The id of the user
		channel_id (int): The id of the channel

	Returns:
		(bool) : Whether the user is a member of the channel
	"""

    channel = get_channel(channel_id)
    return user_id in channel['all_members']


def utc_now():
    """
    Returns the current UTC time in Unix time.

	Parameters:
		None

	Returns:
		(int) : Current UTC Time in Unix time
	"""

    return int(datetime.now(timezone.utc).timestamp())


def get_react(message_id, react_id):
    """
    Returns the react with id react_id.

	Parameters:
		react_id (int): The id of the react
		message_id (int): The id of the message

	Returns:
		react (dict) : Dictionary of react details
		None: If react doesn't exist
	"""

    message = get_message(message_id)
    if message is None:
        return None
    for react in message['reacts']:
        if react_id == react['react_id']:
            return react
    return None


def is_pinned(message_id):
    """
    Returns whether a message is pinned.

	Parameters:
		message_id (int): The id of the message

	Returns:
		(bool): Whether the message is pinned
	"""

    message = get_message(message_id)
    return message['is_pinned']


def has_user_reacted(u_id, message_id, react_id):
    """
    Returns whether a user has reacted to a message using the react
    with id react_id.

	Parameters:
		u_id (int): The id of the user
		message_id (int): The id of the message
		react_id (int): The id of the react

	Returns:
		(bool): Whether the user has reacted to a message using the react
                with id react_id
	"""

    react = get_react(message_id, react_id)
    if react is None:
        return False

    if u_id in react['u_ids']:
        return True
    return False


def get_all_u_id():
    """
    Returns u_ids of all users.

	Parameters:
		None

	Returns:
		(list): List of all u_ids
	"""

    return [user['u_id'] for user in data_store['users']]


def get_permissions():
    """
    Returns a list of valid permissions.

	Parameters:
		None

	Returns:
		(list): List of valid permissions
	"""

    return data_store['permissions'].values()


def user_change_first_last_name(u_id, first_name, last_name):
    """
    Loops through the data store and changes a given user's first and
    last name.

	Parameters:
		u_id (int): The ID of the user
        first_name (str): The first name the user wishes to change to
        last_name (str): The last name the user wishes to change to

	Returns:
		None
	"""

    for user in data_store['users']:
        if user['u_id'] == u_id:
            user['name_first'] = first_name
            user['name_last'] = last_name
            break


def user_change_email(u_id, email):
    """
    Loops through the data store and changes a given user's email.

	Parameters:
		u_id (int): The ID of the user
        email (str): The email the user wants to change to

	Returns:
		None
	"""

    for user in data_store['users']:
        if user['u_id'] == u_id:
            user['email'] = email
            break


def user_check_name(name):
    """
    Checks whether a name is a valid length.

	Parameters:
		name (str): Name to check

	Returns:
		(bool): Whether the name is invalid
	"""

    if 1 <= len(name) <= 50:
        return True
    return False


def is_email_used(email):
    """
    Checks whether an email is being used.

	Parameters:
		email (str): Email to check

	Returns:
		(bool): Whether the email is used or not
	"""

    for user in data_store['users']:
        if user['email'] == email:
            return True
    return False


def is_handle_used(handle):
    """
    Checks if a handle is currently being used.

	Parameters:
		handle (str): User handle to check
	Returns:
		(bool): Whether the handle is used by another user
	"""

    for user in data_store['users']:
        if user['handle_str'] == handle:
            return True
    return False


def handle_length_check(handle):
    """
    Checks if a desired handle is within length guidelines.

	Parameters:
		handle (str): User handle to check
	Returns:
		(bool): Whether the handle is the correct length.
	"""

    return 2 <= len(handle) <= 20


def get_handle(u_id):
    """
    Returns the user's handle as a string.

	Parameters:
		u_id (int): The id of user

	Returns:
		handle_str (str) : The handle of the user
		None: If the user doesn't exist
	"""

    for user in data_store['users']:
        if u_id == user['u_id']:
            return user['handle_str']
    return None


def user_change_handle(u_id, handle):
    """
    Loops through the data store and changes a given user's handle.

	Parameters:
		u_id (int): The ID of the user
        handle (str): The handle the user wants to change to

	Returns:
		None
	"""

    for user in data_store['users']:
        if user['u_id'] == u_id:
            user['handle_str'] = handle
            break


def message_send_message(message_dict, channel_id):
    """
    Loops through the data store to find the correct channel. Will then append
    the message dictionary to the list of messages.

	Parameters:
		message_dict (dict): Dictionary containing the message_id, user_id, the
            message as a string, the time created as a unix timestamp, the
            list of reactions, and if the message is pinned or not
        channel_id (int): The ID of the channel
	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['messages'].append(message_dict)
            break


def message_remove_message(message_dict, channel_id):
    """
    Loops through the data store to find the correct channel. Will then remove
    the message dictionary from the list of messages.

	Parameters:
		message_dict (dict): Dictionary containing the message_id, user_id, the
            message as a string, the time created as a unix timestamp, the
            list of reactions, and if the message is pinned or not
        channel_id (int): The ID of the channel
	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['messages'].remove(message_dict)
            break


def message_edit_message(new_message, message_id, channel_id):
    """
    Loops through the data store to find the correct channel. Then, the
    function will loop through that's channel's messages until it finds
    the matching the message ID. It will then update the message string
    with the new_message.

	Parameters:
		new_message (str): Message the user wishes to change to
        message_id (int): The ID of the message
        channel_id (int): The ID of the channel
	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    message['message'] = new_message
                    break


def message_add_react(react_dict, message_id, channel_id):
    """
    Loops through the data store to find the correct channel. Then, the
    function will loop through that's channel's messages until it finds
    the matching the message ID. It will then append the react dictionary
    to the message information.

	Parameters:
		react_dict (dict): Dictionary containing the ID of the reaction,
            and a list of u_ids that have reacted
        message_id (int): The ID of the message
        channel_id (int): The ID of the channel
	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    message['reacts'].append(react_dict)
                    break


def message_add_react_uid(user_id, message_id, channel_id, react_id):
    """
    Loops through the data store to find the correct channel. Then, the
    function will loop through that's channel's messages until it finds
    the matching the message ID. It will then loop through all reactions
    until it finds the matching react_id. It will then append the user's ID
    to the list of users that have reacted.

	Parameters:
		user_id (int): The ID of the user
        message_id (int): The ID of the message
        channel_id (int): The ID of the channel
        react_id (int): The ID of the reaction
	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    for react in message['reacts']:
                        if react_id == react['react_id']:
                            react['u_ids'].append(user_id)
                            break


def message_remove_react_uid(user_id, message_id, channel_id, react_id):
    """
    Loops through the data store to find the correct channel. Then, the
    function will loop through that's channel's messages until it finds
    the matching the message ID. It will then loop through all reactions
    until it finds the matching react_id. It will then remove the user's ID
    from the list of users that have reacted.

	Parameters:
		user_id (int): The ID of the user
        message_id (int): The ID of the message
        channel_id (int): The ID of the channel
        react_id (int): The ID of the reaction
	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    for react in message['reacts']:
                        if react_id == react['react_id']:
                            react['u_ids'].remove(user_id)
                            break


def message_remove_reaction(react_id, message_id, channel_id):
    """
    Loops through the data store to find the correct channel. Then, the
    function will loop through that's channel's messages until it finds
    the matching the message ID. It will then remove the react dictionary
    from the message information.

	Parameters:
		react_dict (dict): Dictionary containing the ID of the reaction,
            and a list of u_ids that have reacted
        message_id (int): The ID of the message
        channel_id (int): The ID of the channel
	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    for react in message['reacts']:
                        if react_id == react['react_id']:
                            message['reacts'].remove(react)
                            break


def message_pin(message_id, channel_id):
    """
    Loops through the data store to find the correct channel. Then, the
    function will loop through that's channel's messages until it finds
    the matching the message ID. It will then set the status of that
    message's is_pinned to True.

	Parameters:
        message_id (int): The ID of the message
        channel_id (int): The ID of the channel
	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    message['is_pinned'] = True
                    break


def message_unpin(message_id, channel_id):
    """
    Loops through the data store to find the correct channel. Then, the
    function will loop through that's channel's messages until it finds
    the matching the message ID. It will then set the status of that
    message's is_pinned to False.

	Parameters:
        message_id (int): The ID of the message
        channel_id (int): The ID of the channel
	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    message['is_pinned'] = False
                    break


def user_channels(u_id):
    """
    Function that will return a list of channels the user is apart of.

	Parameters:
        u_id (int): The ID of the user
	Return:
		(list): list of channels the user is a member of
	"""
    return [
        channel for channel in data_store['channels']
        if u_id in channel['all_members']
    ]


def channel_search(channel, query_str):
    """
    Function that will return a list of channels the user is apart of.

	Parameters:
        channel (dict): A dictionary containing all of a specific channel's
            info
        query_str (str): The string the user wishes to search for
	Return:
		(list): list of messages containing the string.
	"""

    return [
        message for message in channel['messages']
        if query_str.lower() in message['message'].lower()
    ]


def channel_join(channel_id, u_id):
    """
    Loops through the data_store's channels and finds the channel in which
    the channel_id matches the channel dictionary. It will then append the
    u_id to the list of all_members in that channel.

	Parameters:
		channel_id (int): The ID of the channel
		u_id (int): The ID of the user


	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['all_members'].append(u_id)


def generate_id(id_type):
    """
    Generates ID of id_type. E.g. channel_id, message_id, or react_id.

	Parameters:
		id_type (str): Type of ID to generate

	Returns:
		u_id (int): User ID
	"""

    data_store['max_ids'][id_type] += 1
    return data_store['max_ids'][id_type]


def generate_u_id():
    """
    Generates a user ID.

    Parameters:
        None

	Returns:
		u_id (int): The user ID

	"""
    data_store['max_ids']['u_id'] += 1
    return data_store['max_ids']['u_id']


def generate_message_id():
    """
    Generates a message ID.

	Parameters:
        None
	Returns:
		message_id (int): The message ID
	"""

    message_id = data_store['max_ids']['message_id'] + 1
    data_store['max_ids']['message_id'] = message_id
    return message_id


def get_channel_from_message(message_id):
    """
    Loops through the channels in the data_store. Additionally loops
    through all the messages in the channel until it finds the matching
    message_id. It will return return the channel's dictionary if the
    message_id can be found.

	Parameters:
        message_id (int): The ID of the message
    Returns:
        channel (dict): A dictionary of the channel's information.
        None
	"""

    for channel in data_store['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                return channel
    return None


def get_channel_message(message_id):
    """
    Loops through the channels in the data_store. Additionally loops
    through all the messages in the channel until it finds the matching
    message_id. It will return return the channel's dictionary and the
    message's dictionary if the message_id can be found.

	Parameters:
        message_id (int): The ID of the message
    Returns:
        channel (dict): A dictionary of the channel's information
        message (dict): A dictionary of the message's information
        None
	"""

    for channel in data_store['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                return {'channel': channel, 'message': message}
    return None


def channel_leave(channel_id, u_id):
    """
    Loops through the data_store's channels and finds the channel in which
    the channel_id matches the channel dictionary. It will then remove the
    u_id to the list of all_members in that channel.

	Parameters:
		channel_id (int): The ID of the channel
		u_id (int): The ID of the user


	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['all_members'].remove(u_id)


def channel_leave_owner(channel_id, u_id):
    """
    Loops through the data_store's channels and finds the channel in which
    the channel_id matches the channel dictionary. It will then remove the
    u_id to the list of owener_members in that channel.

	Parameters:
		channel_id (int): The ID of the channel
		u_id (int): The ID of the user


	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['owner_members'].remove(u_id)


def channel_add_owner(channel_id, u_id):
    """
    Loops through the data_store's channels and finds the channel in which
    the channel_id matches the channel dictionary. It will then remove the
    u_id to the list of owener_members in that channel.

	Parameters:
		channel_id (int): The ID of the channel
		u_id (int): The ID of the user


	Returns:
		None
	"""

    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            channel['owner_members'].append(u_id)


def change_permission(u_id, permission_id):
    ''' Given a u_id change their permission_id

    Parameters:
        u_id (int): User ID
        permission_id (int)L: ID of permission level
    '''
    for user in data_store['users']:
        if user['u_id'] == u_id:
            user['permission_id'] = permission_id
            break


def delete_user(u_id):
    ''' Given a u_id delete them from the data_store

    Parameters:
        u_id (int): User ID
    '''

    for channel in data_store['channels']:
        for owner in channel['owner_members']:
            if owner == u_id:
                channel['owner_members'].remove(owner)
                break
        for member in channel['all_members']:
            if member == u_id:
                channel['all_members'].remove(member)
                break
    target_user = get_user(u_id)
    data_store['users'].remove(target_user)


if __name__ == '__main__':
    pass
