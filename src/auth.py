'''
Implementation of auth routes for slackr app
'''
from json import dumps
from flask import request, Blueprint
from error import InputError
from email_validation import invalid_email
from data_store import data_store, User
from token_validation import decode_token, encode_token
import helpers

AUTH = Blueprint('auth', __name__)


@AUTH.route("/auth/register", methods=['POST'])
def route_auth_register():
    '''Flask route for /auth/register'''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']
    return dumps(auth_register(email, password, name_first, name_last))


@AUTH.route("/auth/login", methods=['POST'])
def route_auth_login():
    '''Flask route for /auth/login'''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    return dumps(auth_login(email, password))


@AUTH.route("/auth/logout", methods=['POST'])
def route_auth_logout():
    '''Flask route for /auth/logout'''
    payload = request.get_json()
    token = payload['token']
    return dumps(auth_logout(token))


def auth_register(email, password, name_first, name_last):
    """ Registers a new user

	Parameters:
		email (str): Email of new user
		password (str): Password of new user
		name_first (str): First name of new user
		name_last (str): Last name of new user

	Returns (dict):
		u_id (int): User ID
		token (str): JWT

	"""
    if None in {email, password, name_first, name_last}:
        raise InputError(
            description=
            'Insufficient parameters. Requires email, password, name_first, name_last.'
        )

    if helpers.invalid_password(password):
        raise InputError(
            description='Password entered is less than 6 characters long')

    if helpers.user_check_name(name_first):
        raise InputError(
            description=
            'First name is not between 1 and 50 characters inclusive')

    if helpers.user_check_name(name_last):
        raise InputError(
            description='Last name is not between 1 and 50 characters inclusive'
        )

    if invalid_email(email):
        raise InputError(description='Email entered is not a valid email ')

    if data_store.get_user(email=email) is not None:
        raise InputError(
            description='Email address is already being used by another user')

    user = User(email, password, name_first, name_last)
    data_store.add_user(user)

    return {
        'u_id': user.u_id,
        'token': encode_token(user.u_id),
    }


def auth_login(email, password):
    """ Logs in existing user

	Parameters:
		email (str): Email of user
		password (str): Password of user

	Returns (dict):
		u_id (int): User ID
		token (str): JWT

	"""
    if None in {email, password}:
        raise InputError(
            description='Insufficient parameters. Requires email and password.'
        )

    user = data_store.get_user(email=email)

    if invalid_email(email):
        raise InputError(description='Email entered is not a valid email ')

    if not user:
        raise InputError(description='Email entered does not belong to a user')

    if user.password != helpers.hash_pw(password):
        raise InputError(description='Password is not correct')

    return {'u_id': user.u_id, 'token': encode_token(user.u_id)}


def auth_logout(token):
    """ Logs out user

	Parameters:
		token (str): JWT of session

	Returns (dict):
		is_success (bool): Whether the user has been logged out

	"""
    if token is None:
        raise InputError(
            description='Insufficient parameters. Requires token.')

    decode_token(token)
    data_store.add_to_blacklist(token)

    is_success = token in data_store.token_blacklist

    return {'is_success': is_success}


if __name__ == "__main__":
    pass
