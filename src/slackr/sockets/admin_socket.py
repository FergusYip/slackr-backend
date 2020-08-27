from flask_socketio import emit
from slackr import socketio

from slackr.controllers import admin


@socketio.on('admin_userpermission_change')
def socket_admin_userpermission_change(payload):
    '''Flask route for /admin/userpermission/change'''
    token = payload.get('token')
    u_id = payload.get('u_id')
    permission_id = payload.get('permission_id')
    response = admin.admin_userpermission_change(token, u_id, permission_id)
    emit('permission_changed', response, broadcast=True)


@socketio.on('admin_user_remove')
def socket_admin_user_remove(payload):
    '''Flask route for /admin/userpermission/change'''
    token = payload.get('token')
    u_id = payload.get('u_id')
    response = admin.admin_user_remove(token, u_id)
    emit('user_deleted', response, broadcast=True)
