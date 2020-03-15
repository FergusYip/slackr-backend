import sys
from json import dumps
import jwt
from flask import Flask, request
from flask_cors import CORS
from error import AccessError, InputError

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

SECRET = 'the chunts'

PERMISSIONS = {'owner': 1, 'member': 2}

data_store = {
    'users': [],
    'channels': [],
    'tokens': [],
    'permissions': PERMISSIONS
}


def is_owner(u_id):
    for user in data_store['users']:
        if user['u_id'] is u_id and user['permission_id'] == 1:
            return True
    return False


def permission_values():
    return data_store['permissions'].values()


def user_data(u_id):
    for user in data_store['users']:
        if u_id is user['u_id']:
            return user
    return None


@APP.route("/admin/userpermission/change", methods=['POST'])
def admin_userpermission_change():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    permission_id = request.args.get('permission_id')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Unable to logout due to invalid token')

    if not user_data(u_id):
        raise InputError(description='u_id does not refer to a valid user')

    if permission_id not in permission_values():
        raise InputError(
            description='permission_id does not refer to a valid permission')

    if not is_owner(payload['u_id']):
        raise AccessError(
            description='The authorised user is not an admin or owner')

    user = user_data(u_id)
    user['permission_id'] = permission_id

    return dumps({})


if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
