from data_store import data_store
from datetime import datetime, timezone, timedelta


def get_channel(channel_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            return channel
    return None


def get_message(message_id, channel_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            for message in channel['messages']:
                if message_id == message['message_id']:
                    return message
    return None


def message_existance(message_id, channel_id):
    if get_message(message_id, channel_id) is not None:
        return True
    return False


def get_user(u_id):
    for user in data_store['users']:
        if user['u_id'] == u_id:
            return user
    return None


def is_owner(u_id):
    user = get_user(u_id)
    if user['permission_id'] == data_store['permissions']['owner']:
        return True
    return False


def is_user_admin(u_id, channel_id):
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


def check_message_channel_permissions(message_id, channel_id, u_id):
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']:
            if u_id not in channel['all_members']:
                return False
            else:
                for message in channel['messages']:
                    if message_id == message['message_id']:
                        return True

    return False


def utc_now():
    return int(datetime.now(timezone.utc).timestamp())


def get_react(message_id, channel_id, react_id):
    message = get_message(message_id, channel_id)

    for react in message['reacts']:
        if react_id == react['react_id']:
            return react
            break
    return None


def is_pinned(message_id, channel_id):
    message = get_message(message_id, channel_id)

    if message['is_pinned'] == 1:
        return True
    else:
        return False


def is_channel_member(user_id, channel_id):
    channel = get_channel(channel_id)

    if user_id in channel['all_members']:
        return True
    else:
        return False


def has_user_reacted(user_id, message_id, channel_id, react_id):
    react = get_react(message_id, channel_id, react_id)

    if user_id in react['u_ids']:
        return True
    else:
        return False


def get_all_u_id():
    return [user['u_id'] for user in data_store['users']]


def get_permissions():
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
