'''
Implementation of workspace routes for slackr app
'''
from json import dumps
from datetime import datetime
from flask import Blueprint
from data_store import data_store
from helpers import utc_now

WORKSPACE = Blueprint('workspace', __name__)


@WORKSPACE.route("/workspace/reset", methods=['POST'])
def route_workspace_reset():
    ''' Flask route for /workspace/reset in slackr'''
    return dumps(workspace_reset())


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


if __name__ == "__main__":
    pass
