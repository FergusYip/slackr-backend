import sys
from json import dumps
from flask import Flask, request, Blueprint
from flask_cors import CORS
from error import AccessError, InputError
from data_store import data_store
from token_validation import decode_token
import helpers

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

ADMIN = Blueprint('admin', __name__)


@ADMIN.route("/userpermission/change", methods=['POST'])
def admin_userpermission_change():
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']

    token_payload = decode_token(token)

    if u_id not in helpers.get_all_u_id():
        raise InputError(description='u_id does not refer to a valid user')

    if permission_id not in helpers.get_permissions():
        raise InputError(
            description='permission_id does not refer to a valid permission')

    if not helpers.is_owner(token_payload['u_id']):
        raise AccessError(description='The authorised user is not an owner')

    user = helpers.get_user(u_id)
    user['permission_id'] = permission_id

    return dumps({})


if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
