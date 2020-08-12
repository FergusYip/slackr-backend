from json import dumps
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


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
APP.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/slackr'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(APP)

from slackr import routes