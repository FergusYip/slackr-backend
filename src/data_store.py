import time
import threading
import pickle
from datetime import datetime

SECRET = 'the chunts'

try:
    FILE = open('data_store.p', 'rb')
    data_store = pickle.load(FILE)
except FileNotFoundError:
    data_store = {
        'users': [],
        'channels': [],
        'token_blacklist': [],
        'permissions': {
            'owner': 1,
            'member': 2
        },
        'reactions': {
            'thumbs_up': 1
        },
        'max_ids': {
            'u_id': 0,
            'channel_id': 0,
            'message_id': 0,
        },
        'time_created': int(datetime.utcnow().timestamp())
    }


def save():
    with open('data_store.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)


def autosave():
    timer = threading.Timer(1.0, autosave)
    timer.start()
    save()


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
                'u_ids': [u_id],
            }],
            'is_pinned': is_pinned
        }]
    }],
    'tokens': [],
    'permissions': {
        'owner': 1,
        'member': 2
    }
}

'''

if __name__ == "__main__":
    pass
