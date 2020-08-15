from json import dumps

from flask import Blueprint, request

from slackr.controllers import auth

AUTH_ROUTE = Blueprint('auth', __name__)


@AUTH_ROUTE.route("/auth/register", methods=['POST'])
def route_auth_register():
    '''Flask route for /auth/register'''
    payload = request.get_json()
    email = payload.get('email')
    password = payload.get('password')
    name_first = payload.get('name_first')
    name_last = payload.get('name_last')
    return dumps(auth.auth_register(email, password, name_first, name_last))


@AUTH_ROUTE.route("/auth/login", methods=['POST'])
def route_auth_login():
    '''Flask route for /auth/login'''
    payload = request.get_json()
    email = payload.get('email')
    password = payload.get('password')
    return dumps(auth.auth_login(email, password))


@AUTH_ROUTE.route("/auth/logout", methods=['POST'])
def route_auth_logout():
    '''Flask route for /auth/logout'''
    payload = request.get_json()
    token = payload.get('token')
    return dumps(auth.auth_logout(token))


@AUTH_ROUTE.route("/auth/passwordreset/request", methods=['POST'])
def route_auth_passwordreset_request():
    '''Flask route for /auth/passwordreset/request'''
    payload = request.get_json()
    email = payload.get('email')
    return dumps(auth.auth_passwordreset_request(email))


@AUTH_ROUTE.route("/auth/passwordreset/reset", methods=['POST'])
def route_auth_passwordreset_reset():
    '''Flask route for /auth/logout'''
    payload = request.get_json()
    reset_code = payload.get('reset_code')
    new_password = payload.get('new_password')
    return dumps(auth.auth_passwordreset_reset(reset_code, new_password))
