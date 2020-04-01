'''
Implementation of admin routes for slackr app
'''
from error import AccessError, InputError
from token_validation import decode_token
from data_store import data_store


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
    admin = data_store.get_user(token_payload['u_id'])

    u_id = int(u_id)
    user = data_store.get_user(u_id)

    if u_id not in data_store.u_ids:
        raise InputError(description='u_id does not refer to a valid user')

    if permission_id not in data_store.permission_values:
        raise InputError(
            description='permission_id does not refer to a valid permission')

    if data_store.is_admin(admin) is False:
        raise AccessError(description='The authorised user is not an owner')

    user = data_store.get_user(u_id)
    user.permission_id = permission_id

    return {}


if __name__ == '__main__':
    pass
