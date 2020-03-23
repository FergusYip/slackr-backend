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
    return dumps({})


if __name__ == "__main__":
    pass
