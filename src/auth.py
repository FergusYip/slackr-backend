import hashlib
import jwt
from json import dumps
from flask import Flask, request
from error import AccessError, InputError
from datetime import datetime, timezone

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


def generateToken(u_id):
    global SECRET
    encoded = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')
    return str(encoded)


def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()


def auth_register(email, password, name_first, name_last):
    


def auth_login(email, password):
    
@APP.route("/auth/register", methods=['POST'])
def auth_register():
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


@APP.route("/auth/login", methods=['POST'])
def auth_login():
    global data_store
    for user in data_store['users']:
        if user['email'] == email and user['password'] == hashPassword(
                password):
            return {'u_id': user['u_id'], 'token': generateToken(user['u_id'])}
    return InputError()


@APP.route("/auth/logout", methods=['POST'])
def auth_logout(token):
    global data_store
    if token in data_store['tokens']:
        data_store['tokens'].remove(token)
        return True
    else:
   	    raise AccessError(description='Unable to logout due to invalid token')
    return False




if __name__ == "__main__":
    pass