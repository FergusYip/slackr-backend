'''
Implementation of admin routes for slackr app
'''
from error import AccessError, InputError
from token_validation import decode_token
from data_store import DATA_STORE


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
    admin = DATA_STORE.get_user(token_payload['u_id'])

    u_id = int(u_id)
    user = DATA_STORE.get_user(u_id)

    if u_id not in DATA_STORE.u_ids:
        raise InputError(description='u_id does not refer to a valid user')

    if permission_id not in DATA_STORE.permission_values:
        raise InputError(
            description='permission_id does not refer to a valid permission')

    if DATA_STORE.is_admin(admin) is False:
        raise AccessError(description='The authorised user is not an owner')

    if admin.u_id == u_id and \
        len(DATA_STORE.all_admins) == 1 and \
        permission_id == DATA_STORE.permissions['member']:
        raise InputError(
            description=
            'You must assign another user to be an admin before becoming a member'
        )

    user = DATA_STORE.get_user(u_id)
    user.set_permission_id(permission_id)

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
    admin = DATA_STORE.get_user(token_payload['u_id'])

    u_id = int(u_id)
    target_user = DATA_STORE.get_user(u_id)

    if target_user is None:
        raise InputError(description='u_id does not refer to a valid user')

    if not DATA_STORE.is_admin(admin):
        raise AccessError(description='The authorised user is not an owner')

    if admin.u_id == u_id and len(DATA_STORE.all_admins) == 1:
        raise InputError(
            description=
            'You must assign another user to be an admin before removing yourself'
        )

    DATA_STORE.delete_user(target_user)

    return {}


if __name__ == '__main__':
    pass
