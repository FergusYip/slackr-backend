from json import dumps

from flask import Blueprint, request

from slackr.controllers import admin
from slackr.middleware import auth_middleware

ADMIN_ROUTE = Blueprint('admin', __name__)


@ADMIN_ROUTE.route('/admin/userpermission/change', methods=['POST'])
@auth_middleware
def route_admin_userpermission_change():
    '''Flask route for /admin/userpermission/change'''
    payload = request.get_json()
    token = payload.get('token')
    u_id = payload.get('u_id')
    permission_id = payload.get('permission_id')
    return dumps(admin.admin_userpermission_change(token, u_id, permission_id))


@ADMIN_ROUTE.route('/admin/user/remove', methods=['DELETE'])
@auth_middleware
def route_admin_user_remove():
    '''Flask route for /admin/userpermission/change'''
    payload = request.get_json()
    token = payload.get('token')
    u_id = payload.get('u_id')
    return dumps(admin.admin_user_remove(token, u_id))
