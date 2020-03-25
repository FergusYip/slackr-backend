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

# ======================================================================
# ======================== FLASK ROUTES ================================
# ======================================================================

@USER.route('/profile', methods=['GET'])
def route_user_profile():

    '''
    Flask route to call the user_profile function.
    '''

    token = request.values.get('token')
    target_user = int(request.values.get('u_id'))

    return dumps(user_profile(token, target_user))

@USER.route('/profile/setname', methods=['PUT'])
def route_user_profile_setname():

    '''
    Flask route to call the user_profile_setname function.
    '''

    payload = request.get_json()

    token = payload['token']
    first_name = payload['name_first']
    last_name = payload['name_last']

    return dumps(user_profile_setname(token, first_name, last_name))

@USER.route('/profile/setemail', methods=['PUT'])
def route_user_profile_setemail():

    '''
    Flask route to call the user_profile_setemail function.
    '''

    payload = request.get_json()

    token = payload['token']
    desired_email = payload['email']

    return dumps(user_profile_setemail(token, desired_email))

@USER.route('/profile/sethandle', methods=['PUT'])
def route_user_profile_sethandle():

    '''
    Flask route to call the user_profile_sethandle function.
    '''

    payload = request.get_json()

    token = payload['token']
    desired_handle = payload['handle_str']

    return dumps(user_profile_sethandle(token, desired_handle))

# ======================================================================
# =================== FUNCTION IMPLEMENTATION ==========================
# ======================================================================

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

def user_profile_setemail(token, email):

    '''
    Function that will take a desired email and will change
    the authorized user's information to be updated with this information.
    '''

    token_info = decode_token(token)
    user_id = token_info['u_id']

    user_info = helpers.get_user(user_id)

    if email == user_info['email']:
        # To stop an error occurring when the user either types their current
        # email address, or accidently presses the edit button. Assists with
        # a greater user experience.
        return {}

    if invalid_email(email):
        raise InputError(
            description='Email address is invalid')

    if helpers.is_email_used(email):
        raise InputError(
            description='Email address is already being used by another user')

    helpers.user_change_email(user_id, email)

    return {}

def user_profile_sethandle(token, handle_str):

    '''
    Function that will take a desired handle and will change the authorized
    user's information to reflect this new handle.
    '''

    token_info = decode_token(token)
    user_id = token_info['u_id']

    user_info = helpers.get_user(user_id)

    if handle_str == user_info['handle_str']:
        # To stop an error occurring when the user either types their current
        # handle, or accidently presses the edit button. Assists with a greater
        # user experience.
        return {}

    if not helpers.handle_length_check(handle_str):
        raise InputError(
            description='Handle is not between 2 and 20 characters')

    if helpers.is_handle_used(handle_str):
        raise InputError(
            description='Handle is already being used by another user')

    helpers.user_change_handle(user_id, handle_str)

    return {}

if __name__ == "__main__":
    APP.run(debug=True,
            port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
