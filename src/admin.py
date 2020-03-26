'''
Implementation of admin routes for slackr app
'''
from json import dumps
from flask import request, Blueprint
from error import AccessError, InputError
from token_validation import decode_token
from data_store import data_store

ADMIN = Blueprint('admin', __name__)


@ADMIN.route('/admin/userpermission/change', methods=['POST'])
def route_admin_userpermission_change():
    '''Flask route for /admin/userpermission/change'''
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']
    return dumps(admin_userpermission_change(token, u_id, permission_id))


def admin_userpermission_change(token, u_id, permission_id):
    """ Changes the permission level of a specified user

	Parameters:
		token (str): JWT
		u_id (int): User ID
		permission_id (int): Permission ID

	Returns:
		Empty Dictionary

	"""
    token_payload = decode_token(token)

    if u_id not in data_store.u_ids():
        raise InputError(description='u_id does not refer to a valid user')

    if permission_id not in data_store.get_permissions():
        raise InputError(
            description='permission_id does not refer to a valid permission')

    if not data_store.is_owner(token_payload['u_id']):
        raise AccessError(description='The authorised user is not an owner')

    user = data_store.get_user(u_id)
    user.permission_id = permission_id

    return {}


if __name__ == '__main__':
    pass
