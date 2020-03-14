import sys
import jwt
import math
import hashlib
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import AccessError, InputError
from email_validation import invalid_email

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

SECRET = 'the chunts'

data_store = {'users': [], 'channels': [], 'tokens': []}

def invalid_channel_name(channel_name):
    return len(channel_name) > 20

@APP.route("/channels/list", methods=['GET'])
def channels_list():
    return dumps({
        'channels': [{
            'channel_id': 1,
            'name': 'My Channel',
        }],
    })


@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    token = request.args.get('token')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Token is invalid')

	channels = []
    for channel in data_store['channels']:
		channel_dict = {
			'channel_id': channel['channel_id'],
			'name': channel['name']
		}
		channels.append(channel_dict)

    return dumps({
        'channels': channels
    })


@APP.route("/channels/create", methods=['POST'])
def channels_create():
    token = request.args.get('token')
    name = request.args.get('name')
    is_public =  = request.args.get('is_public')

    try:
        payload = jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Unable to create channel due to invalid token')

    if invalid_channel_name(name):
        raise InputError(description='Name is more than 20 characters long')

    if not data_store['channels']:
        channel_id = 1
    else:
        channel_id = max(data_store['channels']['channel_id']) + 1

    u_id = payload['u_id']

    # Assuming that the user creating the channel automatically joins the channel
    channel = {
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': [u_id],
        'all_members': [u_id],
        'messages': []
    }

    data_store['channels'].append(channel)

    return dumps({
        'channel_id': channel_id
    })


@APP.route("/auth/register", methods=['POST'])
def auth_register():

    email = request.args.get('email')
    password = request.args.get('password')
    name_first = request.args.get('name_first')
    name_last = request.args.get('name_last')

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

    for user in data_store['users']:
        if email == user['email']:
            raise InputError(
                description=
                'Email address is already being used by another user')

    if not data_store['users']:
        u_id = 1
    else:
        u_id = data_store['users'][-1]['u_id'] + 1

    user = {
        'u_id': u_id,
        'email': email,
        'password': hash_pw(password),
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': generate_handle(name_first, name_last)
    }

    data_store['users'].append(user)

    return dumps({
        'u_id': u_id,
        'token': generate_token(u_id),
    })


@APP.route("/auth/login", methods=['POST'])
def auth_login():

    email = request.args.get('email')
    password = request.args.get('password')

    if invalid_email(email):
        raise InputError(description='Email entered is not a valid email ')

    for user in data_store['users']:
        if user['email'] == email and user['password'] == hash_pw(password):
            return dumps({
                'u_id': user['u_id'],
                'token': generate_token(user['u_id'])
            })
        elif user['email'] == email and user['password'] != hash_pw(password):
            raise InputError(description='Password is not correct')

    # If email does not match any user in data store
    raise InputError(description='Email entered does not belong to a user')


@APP.route("/auth/logout", methods=['POST'])
def auth_logout():

    token = request.args.get('token')

    try:
        jwt.decode(token.encode('utf-8'), SECRET)
    except:
        raise AccessError(description='Unable to logout due to invalid token')

    if token in data_store['tokens']:
        data_store['tokens'].remove(token)
        return dumps({'is_success': True})
    else:
        return dumps({'is_success': False})


if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
