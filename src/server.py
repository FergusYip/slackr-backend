import sys
import pickle
from json import dumps
from flask import Flask
from flask_cors import CORS
from admin import ADMIN
from auth import AUTH
from message import MESSAGE
from user import USER
from channels import CHANNELS
from channel import CHANNEL
from other import OTHER
from workspace import WORKSPACE
from standup import STANDUP
from data_store import data_store, autosave

AUTOSAVE_ENABLED = True
DEBUG_MODE = not AUTOSAVE_ENABLED  # Do not change this line


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

APP.register_blueprint(ADMIN)
APP.register_blueprint(AUTH)
APP.register_blueprint(CHANNEL)
APP.register_blueprint(CHANNELS)
APP.register_blueprint(MESSAGE)
APP.register_blueprint(OTHER)
APP.register_blueprint(STANDUP)
APP.register_blueprint(USER)
APP.register_blueprint(WORKSPACE)


@APP.route('/save', methods=['POST'])
def save_state():
    with open('data_store.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({})


@APP.route('/data', methods=['GET'])
def data():
    return dumps(data_store.to_dict())


if __name__ == "__main__":
    if AUTOSAVE_ENABLED:
        autosave()
    APP.run(debug=DEBUG_MODE,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
