'''
Implementation of workspace function for slackr app
'''
from data_store import data_store
from helpers import utc_now


def workspace_reset():
    '''Reset the workspace state'''
    data_store['users'].clear()
    data_store['channels'].clear()
    data_store['token_blacklist'].clear()

    data_store['max_ids']['u_id'] = 0
    data_store['max_ids']['channel_id'] = 0
    data_store['max_ids']['message_id'] = 0

    data_store['time_created'] = utc_now()

    return {}


if __name__ == '__main__':
    pass
