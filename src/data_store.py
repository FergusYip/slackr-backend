SECRET = 'the chunts'

# Permission values
OWNER = 1
MEMBER = 2

DATA_STORE = {
    'users': [],
    'channels': [],
    'token_blacklist': [],
    'permissions': {
        'owner': OWNER,
        'member': MEMBER
    }
}


def get_token_blacklist():
    return DATA_STORE['token_blacklist']


def get_permissions():
    return DATA_STORE['permissions']


def get_users():
    return DATA_STORE['users']


def get_user(u_id):
    for user in get_users():
        if user['u_id'] == u_id:
            return user
    return None


def get_u_ids():
    return [user['u_id'] for user in DATA_STORE['users']]


def get_channels():
    return DATA_STORE['channels']


def get_channel(channel_id):
    for channel in get_channels():
        if channel_id == channel['channel_id']:
            return channel
    return None


def get_messages(channel):
    if channel is None:
        return None

    return channel['messages']


def get_message(channel, message_id):
    if channel is None:
        return None

    for message in channel['messages']:
        if message_id == message['message_id']:
            return message
    return None


def get_reacts(message):
    if message is None:
        return None

    return message['reacts']


'''
Sample Data Store Structure

data_store = {
    'users': [{
            'u_id': u_id,
            'email': email,
            'password': hash_pw(password),
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': generate_handle(name_first, name_last),
            'permission_id': permission_id
        }],
    'channels': [{
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [u_id],
        'all_members': [u_id],
        'messages': [{
            'message_id': message_id,
            'u_id': u_id,
            'message': message,
            'time_created': time_created,
            'reacts': [{
                'react_id': react_id,
                'u_ids': u_id,
                'is_this_user_reacted': is_this_user_reacted
            }],
            'is_pinned': is_pinned
        }]
    }],
    'tokens': [],
    'permissions': {
        'owner': OWNER,
        'member': MEMBER
    }
}

'''

if __name__ == "__main__":
    pass
