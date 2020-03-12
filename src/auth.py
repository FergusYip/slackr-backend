import hashlib
import jwt
from json import dumps
from flask import Flask, request
from error import AccessError, InputError

SECRET = 'Need to decide on something'

DATA = {
    'users': [],
}


def invalid_password(password):
    if len(password) < 6:
        return True
    return False


def invalid_name(name):
    if 1 <= len(name) <= 50:
        return False
    return True


def generateToken(username):
    global SECRET
    encoded = jwt.encode({'username': username}, SECRET, algorithm='HS256')
    print(encoded)
    return str(encoded)


def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()


def auth_register(email, password, name_first, name_last):
    global DATA

    if invalid_password(password) \
        or invalid_name(name_first) \
        or invalid_name(name_last):
        return InputError()

    data['users'].append({
        'username': username,
        'password': hashPassword(password),
    })
    return sendSuccess({
        'token': generateToken(username),
    })


def auth_login(email, password):
    global DATA
    for user in data['users']:
        if user['username'] == username and user['password'] == hashPassword(
                password):
            return sendSuccess({
                'token': generateToken(username),
            })
    return InputError()


def auth_logout(token):
    return {
        'is_success': True,
    }
