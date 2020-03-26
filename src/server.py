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

APP.register_blueprint(ADMIN, url_prefix='/admin')
APP.register_blueprint(AUTH)
APP.register_blueprint(CHANNELS, url_prefix='/channels')
APP.register_blueprint(USER, url_prefix='/user')
APP.register_blueprint(MESSAGE, url_prefix='/message')
APP.register_blueprint(CHANNEL, url_prefix='/channel')
APP.register_blueprint(STANDUP, url_prefix='/standup')
APP.register_blueprint(OTHER)
APP.register_blueprint(WORKSPACE)


@APP.route('/save', methods=['POST'])
def save_state():
    with open('data_store.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({})


@APP.route('/data', methods=['GET'])
def data():
    return dumps(data_store)


'''@APP.route("/user/profile", methods=['GET'])
def user_profile():
    pass


@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname():
    pass


@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail():
    pass


@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_handle():
    pass'''


@APP.route("/standup/start", methods=['POST'])
def standup_start():
    pass


@APP.route("/standup/active", methods=['GET'])
def standup_active():
    pass


@APP.route("/standup/send", methods=['POST'])
def standup_send():
    pass


if __name__ == "__main__":
    if AUTOSAVE_ENABLED:
        autosave()
    APP.run(debug=DEBUG_MODE,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
