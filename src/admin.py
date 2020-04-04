'''
Implementation of admin routes for slackr app
'''
from error import AccessError, InputError
from token_validation import decode_token
import helpers


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

    if u_id not in helpers.get_all_u_id():
        raise InputError(description='u_id does not refer to a valid user')

    if permission_id not in helpers.get_permissions():
        raise InputError(
            description='permission_id does not refer to a valid permission')

    if not helpers.is_owner(token_payload['u_id']):
        raise AccessError(description='The authorised user is not an owner')

    helpers.change_permission(u_id, permission_id)

    return {}


def admin_user_remove(token, u_id):
    """ Given a User by their user ID, remove the user

	Parameters:
		token (str): JWT
		u_id (int): User ID

	Returns:
		Empty Dictionary

	"""
    token_payload = decode_token(token)

    if u_id not in helpers.get_all_u_id():
        raise InputError(description='u_id does not refer to a valid user')

    if not helpers.is_owner(token_payload['u_id']):
        raise AccessError(description='The authorised user is not an owner')

    helpers.change_permission(u_id, permission_id)


if __name__ == '__main__':
    pass
