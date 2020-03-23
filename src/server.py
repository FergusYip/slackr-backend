import sys
import pickle
import time
import threading
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from auth import AUTH
from channels import CHANNELS
from other import OTHER
from admin import admin
from workspace import workspace
from data_store import data_store


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

APP.register_blueprint(admin, url_prefix='/admin')
APP.register_blueprint(AUTH, url_prefix='/auth')
APP.register_blueprint(CHANNELS, url_prefix='/channels')
APP.register_blueprint(OTHER)
APP.register_blueprint(workspace)


def load_state():
    try:
        file = open('data_store.p', 'rb')
        data_store = pickle.load(file)
    except FileNotFoundError:
        data_store = {'users': [], 'channels': [], 'tokens': []}


def auto_save():
    while True:
        pickle.dump(data_store, open('data_store.p', 'wb'))
        time.sleep(1)


def thread_save():
    auto_save_thread = threading.Thread(target=auto_save)
    auto_save_thread.start()


@APP.route('/save', methods=['POST'])
def save_state():
    with open('data_store.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)


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
    load_state()
    thread_save()
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
