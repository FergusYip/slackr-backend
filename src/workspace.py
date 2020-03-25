from json import dumps
from flask import Blueprint
from data_store import data_store
from datetime import datetime

WORKSPACE = Blueprint('workspace', __name__)


@WORKSPACE.route("/workspace/reset", methods=['POST'])
def workspace_reset():
    '''Reset the workspace state'''
    data_store.reset()

    return dumps({})


if __name__ == "__main__":
    pass
