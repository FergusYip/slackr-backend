'''
Function to reset the state of the Slackr application.
'''

from slackr import db


def workspace_reset():
    '''Reset the workspace state'''
    db.drop_all()
    db.create_all()
    return {}


if __name__ == '__main__':
    pass
