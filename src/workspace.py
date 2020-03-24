from json import dumps
from flask import Blueprint
from data_store import data_store

WORKSPACE = Blueprint('workspace', __name__)


@WORKSPACE.route("/workspace/reset", methods=['POST'])
def workspace_reset():
    '''Reset the workspace state'''
    data_store['users'].clear()
    data_store['channels'].clear()
    data_store['token_blacklist'].clear()

    data_store['max_ids']['u_id'] = 0
    data_store['max_ids']['channel_id'] = 0
    data_store['max_ids']['message_id'] = 0

    return dumps({})


if __name__ == "__main__":
    pass
