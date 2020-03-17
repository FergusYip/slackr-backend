import sys
from json import dumps
import jwt
from flask import Flask, request, Blueprint
from flask_cors import CORS
from error import AccessError, InputError
from data_store import data_store, SECRET, OWNER, MEMBER

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

admin = Blueprint('admin', __name__)


def is_owner(u_id):
    for user in data_store['users']:
        if user['u_id'] is u_id and user['permission_id'] is OWNER:
            return True
    return False


def permission_values():
    return data_store['permissions'].values()


def user_data(u_id):
    for user in data_store['users']:
        if u_id is user['u_id']:
            return user
    return None


def all_u_id():
    return [user['u_id'] for user in data_store['users']]


@admin.route("/userpermission/change", methods=['POST'])
def admin_userpermission_change():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    permission_id = int(request.args.get('permission_id'))

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Unable to logout due to invalid token')

    if u_id not in all_u_id():
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
