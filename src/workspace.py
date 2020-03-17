import sys
from json import dumps
from flask import Flask, Blueprint
from flask_cors import CORS
from data_store import data_store

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

workspace = Blueprint('workspace', __name__)


@workspace.route("/workspace/reset", methods=['POST'])
def workspace_reset():
    '''Reset the workspace state'''
    data_store['users'].clear()
    data_store['channels'].clear()
    data_store['token_blacklist'].clear()
    return dumps({})


if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
