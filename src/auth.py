import math
import hashlib
from json import dumps
from flask import request, Blueprint
from error import InputError
from email_validation import invalid_email
from data_store import data_store
from token_validation import decode_token, encode_token

AUTH = Blueprint('auth', __name__)


def invalid_password(password):
    if len(password) < 6:
        return True
    return False


def invalid_name(name):
    if 1 <= len(name) <= 50:
        return False
    return True


def get_user(email):
    for user in data_store['users']:
        if email == user['email']:
            return user
    return None


def generate_u_id():
    data_store['max_ids']['u_id'] += 1
    return data_store['max_ids']['u_id']


def set_default_permission():
    if not data_store['users']:
        return data_store['permissions']['owner']
    else:
        return data_store['permissions']['member']


def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()


def is_unique_handle(handle_str):
    for user in data_store['users']:
        if user['handle_str'] is handle_str:
            return False
    return True


def generate_handle(name_first, name_last):
    concatentation = name_first.lower() + name_last.lower()
    handle_str = concatentation[:20]

    unique_modifier = 0
    while not is_unique_handle(handle_str):
        split_handle = list(handle_str)

        # Remove n number of characters from split_handle
        unique_digits = int(math.log10(unique_modifier)) + 1
        for _ in range(unique_digits):
            split_handle.pop()

        split_handle.append(str(unique_modifier))
        handle_str = ''.join(split_handle)

        unique_modifier += 1

    return handle_str


def auth_register(email, password, name_first, name_last):
    if not email or not password or not name_first or not name_last:
        raise InputError(
            description=
            'Insufficient parameters. Requires email, password, name_first, name_last.'
        )

    if invalid_password(password):
        raise InputError(
            description='Password entered is less than 6 characters long')

    if invalid_name(name_first):
        raise InputError(
            description=
            'First name is not between 1 and 50 characters inclusive')

    if invalid_name(name_last):
        raise InputError(
            description='Last name is not between 1 and 50 characters inclusive'
        )

    if invalid_email(email):
        raise InputError(description='Email entered is not a valid email ')

    if get_user(email) is not None:
        raise InputError(
            description='Email address is already being used by another user')

    u_id = generate_u_id()
    user = {
        'u_id': u_id,
        'email': email,
        'password': hash_pw(password),
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': generate_handle(name_first, name_last),
        'permission_id': set_default_permission(),
    }

    data_store['users'].append(user)

    return {
        'u_id': u_id,
        'token': encode_token(u_id),
    }


@AUTH.route("/register", methods=['POST'])
def route_auth_register():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']
    return dumps(auth_register(email, password, name_first, name_last))


def auth_login(email, password):
    if not email or not password:
        raise InputError(
            description='Insufficient parameters. Requires email and password.'
        )

    user = get_user(email)

    if invalid_email(email):
        raise InputError(description='Email entered is not a valid email ')

    if not user:
        raise InputError(description='Email entered does not belong to a user')

    if user['password'] != hash_pw(password):
        raise InputError(description='Password is not correct')

    return {'u_id': user['u_id'], 'token': encode_token(user['u_id'])}


@AUTH.route("/login", methods=['POST'])
def route_auth_login():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    return dumps(auth_login(email, password))


def auth_logout(token):
    if not token:
        raise InputError(
            description='Insufficient parameters. Requires token.')

    decode_token(token)
    data_store['token_blacklist'].append(token)

    if token in data_store['token_blacklist']:
        is_success = False
    else:
        is_success = False

    return {'is_success': is_success}


@AUTH.route("/logout", methods=['POST'])
def route_auth_logout():
    payload = request.get_json()
    token = payload['token']
    return dumps(auth_logout(token))


if __name__ == "__main__":
    pass