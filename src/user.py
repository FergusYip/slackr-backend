'''
Functionality for users of the program to get other user's profile information,
as well as change their own personal information.
'''

import sys
from json import dumps
from flask import Flask, request, Blueprint
from flask_cors import CORS
from error import InputError
from email_validation import invalid_email
from token_validation import decode_token
import helpers

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

USER = Blueprint('user', __name__)

@USER.route('/profile', methods=['GET'])
def route_user_profile():

    '''
    Flask route to call the user_profile function.
    '''

    token = request.values.get('token')
    target_user = int(request.values.get('u_id'))

    return dumps(user_profile(token, target_user))

def user_profile_setname(token, first_name, last_name):

    '''
    Function that will take a desired first and last name and will change
    the authorized user's information to be updated with this information.
    '''

    token_info = decode_token(token)
    user_id = token_info['u_id']

    if not helpers.user_check_name(first_name):
        raise InputError(
            description='First name is not between 1 and 50 characters')

    if not helpers.user_check_name(last_name):
        raise InputError(
            description='Last name is not between 1 and 50 characters')

    helpers.user_change_first_last_name(user_id, first_name, last_name)

    return {}

@USER.route('/profile/setname', methods=['PUT'])
def route_user_profile_setname():

    '''
    Flask route to call the user_profile function.
    '''

    payload = request.get_json()
    
    token = payload['token']
    first_name = payload['name_first']
    last_name = payload['name_last']

    return dumps(user_profile_setname(token, first_name, last_name))

@USER.route('/profile/setemail', methods=['PUT'])
def user_profile_setemail():

    '''
    Function that will take a desired email and will change
    the authorized user's information to be updated with this information.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    desired_email = payload['email']

    if invalid_email(desired_email):
        raise InputError(
            description='Email address is invalid')

    if helpers.is_email_used(desired_email):
        raise InputError(
            description='Email address is already being used by another user')

    helpers.user_change_email(user_id, desired_email)

    return dumps({})

@USER.route('/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():

    '''
    Function that will take a desired handle and will change the authorized
    user's information to reflect this new handle.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    desired_handle = payload['handle_str']

    if not helpers.handle_length_check(desired_handle):
        raise InputError(
            description='Handle is not between 2 and 20 characters')

    if helpers.is_handle_used(desired_handle):
        raise InputError(
            description='Handle is already being used by another user')

    helpers.user_change_handle(user_id, desired_handle)

    return dumps({})

def user_profile(token, target_uid):

    '''
    Function that will return the profile information of a desired
    user on the Slackr platform.
    '''

    # By calling the decode function, multiple error checks are performed.
    decode_token(token)

    if helpers.get_user(target_uid) is None:
        raise InputError(
            description='User ID is not a valid user')

    user_info = helpers.get_user(target_uid)

    user_return = {
        'u_id': user_info['u_id'],
        'email': user_info['email'],
        'name_first': user_info['name_first'],
        'name_last': user_info['name_last'],
        'handle_str': user_info['handle_str']
    }

    return user_return

if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
