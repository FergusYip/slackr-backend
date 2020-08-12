'''
Function to reset the state of the Slackr application.
'''

import os
import glob
from slackr import db


def workspace_reset():
    '''Reset the workspace state'''
    db.drop_all()
    db.create_all()

    for file in glob.glob('src/profile_images/*.jpg'):
        if os.path.exists(file):
            os.remove(file)

    return {}


if __name__ == '__main__':
    pass
