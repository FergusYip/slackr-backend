import sys
import jwt
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import AccessError, InputError

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

SECRET = 'the chunts'

data_store = {'users': [], 'channels': [], 'tokens': []}


@APP.route("/users/all", methods=['GET'])
def users_all():
    token = request.args.get('token')
    try:
        jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Invalid token')

    users = []
    for user in data_store['users']:
        user_dict = {
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
        }
        users.append(user_dict)

    return dumps({'users': users})

@APP.route("/search", methods=['GET'])
def search():
    pass

if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
