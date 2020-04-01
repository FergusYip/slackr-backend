'''
Implementation of workspace function for slackr app
'''
from data_store import data_store


def workspace_reset():
    '''Reset the workspace state'''
    data_store.reset()
    return {}


if __name__ == '__main__':
    pass
