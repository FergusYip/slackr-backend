'''
Implementation of workspace function for slackr app
'''
from data_store import DATA_STORE


def workspace_reset():
    '''Reset the workspace state'''
    DATA_STORE.reset()
    return {}


if __name__ == '__main__':
    pass
