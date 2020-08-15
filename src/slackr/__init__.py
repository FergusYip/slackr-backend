from json import dumps

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from slackr.utils.constants import DATABASE_URL


def default_handler(err):
    '''Default handler for errors'''
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
APP.register_error_handler(Exception, default_handler)
APP.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(APP)

from slackr.routes.admin_route import ADMIN_ROUTE
from slackr.routes.auth_route import AUTH_ROUTE
from slackr.routes.channel_route import CHANNEL_ROUTE
from slackr.routes.channels_route import CHANNELS_ROUTE
from slackr.routes.hangman_route import HANGMAN_ROUTE
from slackr.routes.img_url_route import IMG_URL_ROUTE
from slackr.routes.message_route import MESSAGE_ROUTE
from slackr.routes.other_route import OTHER_ROUTE
from slackr.routes.standup_route import STANDUP_ROUTE
from slackr.routes.user_route import USER_ROUTE
from slackr.routes.workspace_route import WORKSPACE_ROUTE

APP.register_blueprint(ADMIN_ROUTE)
APP.register_blueprint(AUTH_ROUTE)
APP.register_blueprint(CHANNEL_ROUTE)
APP.register_blueprint(CHANNELS_ROUTE)
APP.register_blueprint(HANGMAN_ROUTE)
APP.register_blueprint(IMG_URL_ROUTE)
APP.register_blueprint(MESSAGE_ROUTE)
APP.register_blueprint(OTHER_ROUTE)
APP.register_blueprint(STANDUP_ROUTE)
APP.register_blueprint(USER_ROUTE)
APP.register_blueprint(WORKSPACE_ROUTE)
