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


def invalid_password(password):
    ''' Checks whether a password is invalid

	Parameters:
		password (str): Password

	Returns:
		(bool): Whether the password is invalid

	'''
    return len(password) < 6


if __name__ == '__main__':
    pass
