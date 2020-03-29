'''Backend server file for slackr'''
import sys
from json import dumps
from flask import Flask
from flask_cors import CORS
from admin import ADMIN
from auth import AUTH
from channel import CHANNEL
from channels import CHANNELS
from message import MESSAGE
from other import OTHER
from standup import STANDUP
from user import USER
from workspace import WORKSPACE
from data_store import autosave

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
APP.register_blueprint(CHANNELS)
APP.register_blueprint(USER, url_prefix='/user')
APP.register_blueprint(MESSAGE, url_prefix='/message')
APP.register_blueprint(CHANNEL)
APP.register_blueprint(STANDUP, url_prefix='/standup')
APP.register_blueprint(OTHER)
APP.register_blueprint(WORKSPACE)

if __name__ == "__main__":
    if AUTOSAVE_ENABLED:
        autosave()
    APP.run(debug=DEBUG_MODE,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
