import sys
import pickle
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from admin import ADMIN
from auth import AUTH
from channels import CHANNELS
from other import OTHER
from workspace import WORKSPACE
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

APP.register_blueprint(ADMIN, url_prefix='/admin')
APP.register_blueprint(AUTH, url_prefix='/auth')
APP.register_blueprint(CHANNELS, url_prefix='/channels')
APP.register_blueprint(OTHER)
APP.register_blueprint(WORKSPACE)


def load_state():
    try:
        FILE = open('data_store.p', 'rb')
        data_store = pickle.load(FILE)
    except Exception:
        data_store = {'users': [], 'channels': [], 'tokens': []}


@APP.route('/save', methods=['POST'])
def save_state():
    with open('data_store.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)


@APP.route('/data', methods=['GET'])
def data():
    return dumps(data_store)


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({'data': data})


@APP.route("/channel/invite", methods=['POST'])
def channel_invite():
    pass


@APP.route("/channel/details", methods=['GET'])
def channel_details():
    pass


@APP.route("/channel/messages", methods=['GET'])
def channel_messages():
    pass


@APP.route("/channel/leave", methods=['POST'])
def channel_leave():
    pass


@APP.route("/channel/join", methods=['POST'])
def channel_join():
    pass


@APP.route("/channel/addowner", methods=['POST'])
def channel_addowner():
    pass


@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowner():
    pass


@APP.route("/message/send", methods=['POST'])
def message_send():
    pass


@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater():
    pass


@APP.route("/message/react", methods=['POST'])
def message_react():
    pass


@APP.route("/message/unreact", methods=['POST'])
def message_unreact():
    pass


@APP.route("/message/pin", methods=['POST'])
def message_pin():
    pass


@APP.route("/message/unpin", methods=['POST'])
def message_unpin():
    pass


@APP.route("/message/remove", methods=['DELETE'])
def message_remove():
    pass


@APP.route("/message/edit", methods=['PUT'])
def message_edit():
    pass


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


@APP.route("/workspace/reset", methods=['POST'])
def workspace_reset():
    pass


if __name__ == "__main__":
    load_state()
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
