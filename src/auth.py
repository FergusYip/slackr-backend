import hashlib
import jwt
from json import dumps
from flask import Flask, request
from error import AccessError, InputError

SECRET = 'the chunts'

data_store = {}


def invalid_password(password):
    if len(password) < 6:
        return True
    return False


def invalid_name(name):
    if 1 <= len(name) <= 50:
        return False
    return True


def generateToken(u_id):
    global SECRET
    encoded = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')
    return str(encoded)


def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()


def auth_register(email, password, name_first, name_last):
    global data_store
    if invalid_password(password) \
        or invalid_name(name_first) \
        or invalid_name(name_last):
        return InputError()

    # user = {
    #     'u_id': None,
    #     'email': email,
    #     'password': hashPassword(password),
    #     'name_first': name_first,
    #     'name_last': name_last,
    #     'handle_str':
    # }

    data['users'].append({
        'username': username,
        'password': hashPassword(password),
    })
    return sendSuccess({
        'token': generateToken(username),
    })


def auth_login(email, password):
    global data_store
    for user in data_store['users']:
        if user['email'] == email and user['password'] == hashPassword(
                password):
            return {'u_id': user['u_id'], 'token': generateToken(user['u_id'])}
    return InputError()


def auth_logout(token):
    return {
        'is_success': True,
    }


if __name__ == "__main__":
    pass