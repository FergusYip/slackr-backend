'''
Function to reset the state of the Slackr application.
'''

from data_store import DATA_STORE


def workspace_reset():
    '''Reset the workspace state'''
    DATA_STORE.reset()
    return {}


if __name__ == '__main__':
    pass
