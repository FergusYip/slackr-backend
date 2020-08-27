'''
Functions to provide administrative management tools on the program. Will
allow admins to change user permissions and delete users.
'''

from slackr.error import AccessError, InputError
from slackr.token_validation import decode_token
from slackr.models.user import User
from slackr import db
from slackr.utils.constants import PERMISSIONS


def admin_is_admin(token):
    if None in {token}:
        raise InputError(description='Insufficient parameters')

    token_payload = decode_token(token)
    u_id = token_payload['u_id']
    user = User.query.get(u_id)

    if user is None:
        raise InputError(description='u_id does not refer to a valid user')

    return {'is_admin': user.permission_id == PERMISSIONS['owner']}


def admin_userpermission_change(token, u_id, permission_id):
    """ Changes the permission level of a specified user

	Parameters:
		token (str): JWT
		u_id (int): User ID
		permission_id (int): Permission ID

	Returns:
		Empty Dictionary

	"""

    if None in {token, u_id, permission_id}:
        raise InputError(description='Insufficient parameters')

    token_payload = decode_token(token)
    admin_u_id = token_payload['u_id']

    admin = User.query.get(admin_u_id)
    user = User.query.get(u_id)

    if user is None:
        raise InputError(description='u_id does not refer to a valid user')

    if permission_id not in PERMISSIONS.values():
        raise InputError(
            description='permission_id does not refer to a valid permission')

    if admin.permission_id != PERMISSIONS['owner']:
        raise AccessError(description='The authorised user is not an owner')

    admin_users = User.query.filter_by(
        permission_id=PERMISSIONS['owner']).all()

    if admin_u_id == u_id and \
        len(admin_users) == 1 and permission_id == PERMISSIONS['member']:
        raise InputError(
            description=
            'You must assign another user to be an admin before becoming a member'
        )

    user.permission_id = permission_id
    db.session.commit()

    return {}


def admin_user_remove(token, u_id):
    ''' Given a User by their user ID, remove the user

	Parameters:
		token (str): JWT
		u_id (int): User ID

	Returns:
		Empty Dictionary

	'''

    if None in {token, u_id}:
        raise InputError(description='Insufficient parameters')

    token_payload = decode_token(token)
    admin_u_id = token_payload['u_id']

    admin = User.query.get(admin_u_id)
    target_user = User.query.get(u_id)

    if target_user is None:
        raise InputError(description='u_id does not refer to a valid user')

    if admin.permission_id != PERMISSIONS['owner']:
        raise AccessError(description='The authorised user is not an owner')

    admin_users = User.query.filter_by(
        permission_id=PERMISSIONS['owner']).all()

    if admin.u_id == u_id and len(admin_users) == 1:
        raise InputError(
            description=
            'You must assign another user to be an admin before removing yourself'
        )

    db.session.delete(target_user)
    db.session.commit()

    return {}


if __name__ == '__main__':
    pass
