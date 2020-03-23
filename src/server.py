import sys
import pickle
from json import dumps
from flask import Flask
from flask_cors import CORS
from auth import AUTH
from channels import CHANNELS
from other import OTHER
from admin import ADMIN
from workspace import workspace
from data_store import data_store, autosave


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
APP.register_blueprint(AUTH, url_prefix='/auth')
APP.register_blueprint(CHANNELS, url_prefix='/channels')
APP.register_blueprint(OTHER)
APP.register_blueprint(workspace)


@APP.route('/save', methods=['POST'])
def save_state():
    with open('data_store.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)
    return dumps({})


@APP.route('/data', methods=['GET'])
def data():
    return dumps(data_store)


@APP.route("/user/profile", methods=['GET'])
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
    pass


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
    autosave()
    APP.run(debug=False,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
