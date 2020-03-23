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

@USER.route('/profile', methods='GET')
def user_profile():

    '''
    Function that will return the profile information of a desired
    user on the Slackr platform.
    '''

    payload = request.get_json()

    token = payload['token']

    # By calling the decode function, multiple error checks are performed.
    decode_token(token)

    # The user ID of the person you want information for.
    target_user = payload['u_id']

    if not helpers.get_user(target_user):
        raise InputError(
            description='User ID is not a valid user')

    user_info = helpers.get_user(target_user)

    return dumps(user_info)

@USER.route('/profile/setname', methods='PUT')
def user_profile_setname():

    '''
    Function that will take a desired first and last name and will change
    the authorized user's information to be updated with this information.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    first_name = payload['name_first']
    last_name = payload['name_last']

    if not helpers.user_check_name(first_name):
        raise InputError(
            description='First name is not between 1 and 50 characters')

    if not helpers.user_check_name(last_name):
        raise InputError(
            description='Last name is not between 1 and 50 characters')

    helpers.user_change_first_last_name(user_id, first_name, last_name)

    return dumps({})

@USER.route('/profile/setemail', methods='PUT')
def user_profile_setemail(token, email):

    '''
    Function that will take a desired email and will change
    the authorized user's information to be updated with this information.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    desired_email = email

    if invalid_email(desired_email):
        raise InputError(
            description='Email address is invalid')

    if helpers.is_email_used(desired_email):
        raise InputError(
            description='Email address is already being used by another user')

    helpers.user_change_email(user_id, desired_email)

    return dumps({})

@USER.route('/profile/sethandle', methods='PUT')
def user_profile_sethandle(token, handle_str):

    '''
    Function that will take a desired handle and will change the authorized
    user's information to reflect this new handle.
    '''

    payload = request.get_json()

    token = payload['token']
    token_info = decode_token(token)
    user_id = token_info['u_id']

    desired_handle = handle_str

    if not helpers.handle_length_check(desired_handle):
        raise InputError(
            description='Handle is not between 2 and 20 characters')

    if helpers.is_handle_used(desired_handle):
        raise InputError(
            description='Handle is already being used by another user')

    helpers.user_change_handle(user_id, desired_handle)

    return dumps({})

if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
