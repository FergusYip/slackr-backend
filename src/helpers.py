''' Helper module with functions to access values from data_store'''
import hashlib
from datetime import datetime, timezone


def utc_now():
    '''
    Returns the current UTC time in Unix time.

	Parameters:
		None

	Returns:
		(int) : Current UTC Time in Unix time
	'''

    return int(datetime.now(timezone.utc).timestamp())


def hash_pw(password):
    ''' Returns a hashed password

	Parameters:
		password (str): Password

	Returns:
		hashed password (str): Hashed password

	'''
    return hashlib.sha256(password.encode()).hexdigest()


"""
The following functions must be moved to data_store.py


def delete_user(u_id):
    ''' Given a u_id delete them from the data_store

    Parameters:
        u_id (int): User ID
    '''

    for channel in data_store['channels']:
        for owner in channel['owner_members']:
            if owner == u_id:
                channel['owner_members'].remove(owner)
                break
        for member in channel['all_members']:
            if member == u_id:
                channel['all_members'].remove(member)
                break
    target_user = get_user(u_id)
    data_store['users'].remove(target_user)


def change_password(u_id, password):
    ''' Given a u_id and password, change the password of the user

    Parameters:
        u_id (int): User ID
        password(str): Desired password
    '''
    for user in data_store['users']:
        if user['u_id'] == u_id:
            user['password'] = hash_pw(password)
            break


def make_reset_request(reset_code, u_id):
    ''' Make a reset_request

    Parameters:
        reset_code (int): Reset code
        u_id (int): Requested user

    '''

    reset_request = {'reset_code': reset_code, 'u_id': u_id}
    data_store['reset_requests'].append(reset_request)


def invalidate_reset_request(reset_code):
    ''' Invalidate a reset_request

    Parameters:
        reset_code (int): Reset code

    '''

    for request in data_store['reset_requests']:
        if request['reset_code'] == reset_code:
            data_store['reset_requests'].remove(request)


def invalidate_reset_request_from_user(u_id):
    ''' Invalidates all reset requests made by a user

    Parameters:
        u_id (int): User ID

    '''

    for request in data_store['reset_requests']:
        if request['u_id'] == u_id:
            data_store['reset_requests'].remove(request)


def get_reset_request(reset_code):
    ''' Given a reset_code, get the associated request

    Parameters:
        reset_code (int): Reset code

    Returns (dict):
        reset_code (int): Reset code
        u_id (int): Requested user
    '''
    for request in data_store['reset_requests']:
        if request['reset_code'] == reset_code:
            return request
    return None


def get_owners():
    ''' Returns a list of owners

    Returns:
        u_ids (list): List of user IDs
    '''

    return [
        user['u_id'] for user in data_store['users']
        if user['permission_id'] == data_store['permissions']['owner']
    ]


def change_profile_image_url(u_id, profile_img_url):

    for user in data_store['users']:
        if user['u_id'] == u_id:
            user['profile_img_url'] = profile_img_url

"""

if __name__ == '__main__':
    pass
