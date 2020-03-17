SECRET = 'the chunts'

# Permission values
OWNER = 1
MEMBER = 2

data_store = {
    'users': [],
    'channels': [],
    'tokens': [],
    'permissions': {
        'owner': OWNER,
        'member': MEMBER
    }
}

EMPTY_DATA_STORE = {
    'users': [],
    'channels': [],
    'tokens': [],
    'permissions': {
        'owner': OWNER,
        'member': MEMBER
    }
}
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
            'reacts': reacts, <- I assume this is a list
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