''' Data Store for the slackr backend'''
import threading
import pickle
from datetime import datetime

SECRET = 'the chunts'

try:
    data_store = pickle.load(open('data_store.p', 'rb'))
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
    '''Save the state of the data_store into a pickle'''
    pickle.dump(data_store, open('data_store.p', 'wb'))


def autosave():
    '''Thread to save state every second'''
    timer = threading.Timer(1.0, autosave)
    timer.start()
    save()


if __name__ == "__main__":
    pass
