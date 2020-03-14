import hashlib
import jwt
from json import dumps
from flask import Flask, request
from error import AccessError, InputError
from datetime import datetime, timezone
import math

SECRET = 'the chunts'

data_store = {}


def utc_now():
    return int(datetime.now(timezone.utc).timestamp())


def invalid_password(password):
    if len(password) < 6:
        return True
    return False


def invalid_name(name):
    if 1 <= len(name) <= 50:
        return False
    return True


def generate_token(u_id):
    global SECRET
    encoded = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')
    return str(encoded)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def is_unique_handle(handle_str):
    for user in data_store['users']:
        if user['handle_str'] is handle_str:
            return False
    return True


def generate_handle(name_first, name_last):
    global data_store

    concatentation = name_first.lower() + name_last.lower()
    handle_str = concatentation[:20]

    unique_modifier = 0
    while not is_unique_handle(handle_str):
        split_handle = list(handle_str)

        # Remove n number of characters from split_handle
        unique_digits = int(math.log10(unique_modifier)) + 1
        for n in range(unique_digits):
            split_handle.pop()

        split_handle.append(str(unique_modifier))
        handle_str = ''.join(split_handle)

        unique_modifier += 1

    return handle_str


@APP.route("/auth/register", methods=['POST'])
def auth_register(email=request.args.get('email'),
                  password=request.args.get('password'),
                  name_first=request.args.get('name_first'),
                  name_last=request.args.get('name_last')):

    global data_store

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

    for user in data_store['users']:
        if email == user[email]:
            raise InputError(
                description=
                'Email address is already being used by another user')

    u_id = data_store['users'][-1]['u_id'] + 1

    user = {
        'u_id': u_id,
        'email': email,
        'password': hashPassword(password),
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': generate_handle(name_first, name_last)
    }

    data_store['users'].append(user)

    return {
        'u_id': u_id,
        'token': generateToken(username),
    }


@APP.route("/auth/login", methods=['POST'])
def auth_login(email=request.args.get('email'),
               password=request.args.get('password')):
    global data_store
    for user in data_store['users']:
        if user['email'] == email and user['password'] == hashPassword(
                password):
            return {'u_id': user['u_id'], 'token': generateToken(user['u_id'])}
    return InputError()


@APP.route("/auth/logout", methods=['POST'])
def auth_logout(token=request.args.get('token')):
    global data_store
    if token in data_store['tokens']:
        data_store['tokens'].remove(token)
        return True
    else:
        raise AccessError(description='Unable to logout due to invalid token')
    return False


if __name__ == "__main__":
    pass