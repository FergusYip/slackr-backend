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
    for channel in data_store['channels']:
        if channel_id == channel['channel_id']
            for message in data_store['channels']['messages']:
                if message_id == message['message_id']:
                    return True
    return False

def get_user(u_id):
    for user in data_store['users']:
        if user['u_id'] == u_id:
            return user
    return None

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
