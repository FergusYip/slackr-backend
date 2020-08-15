from json import dumps

from flask import Blueprint, request

from slackr.controllers import user
from slackr.middleware import auth_middleware

USER_ROUTE = Blueprint('user', __name__)


@USER_ROUTE.route('/user/profile', methods=['GET'])
@auth_middleware
def route_USER_ROUTE():
    '''Flask route for /user/profile'''
    token = request.values.get('token')
    target_user = request.values.get('u_id')
    return dumps(user.user_profile(token, target_user))


@USER_ROUTE.route('/user/profile/setname', methods=['PUT'])
@auth_middleware
def route_user_setname():
    '''Flask route for /user/profile/setname'''
    payload = request.get_json()
    token = payload.get('token')
    first_name = payload.get('name_first')
    last_name = payload.get('name_last')
    return dumps(user.user_profile_setname(token, first_name, last_name))


@USER_ROUTE.route('/user/profile/setemail', methods=['PUT'])
@auth_middleware
def route_user_setemail():
    '''Flask route for /user/profile/setemail'''
    payload = request.get_json()
    token = payload.get('token')
    desired_email = payload.get('email')
    return dumps(user.user_profile_setemail(token, desired_email))


@USER_ROUTE.route('/user/profile/sethandle', methods=['PUT'])
@auth_middleware
def route_user_sethandle():
    '''Flask route for /user/profile/sethandle'''
    payload = request.get_json()
    token = payload.get('token')
    desired_handle = payload.get('handle_str')
    return dumps(user.user_profile_sethandle(token, desired_handle))


@USER_ROUTE.route('/user/profile/uploadphoto', methods=['POST'])
@auth_middleware
def route_user_profile_uploadphoto():
    '''Flask route for /user/profile/uploadphoto'''
    payload = request.get_json()
    token = payload.get('token')
    img_url = payload.get('img_url')
    x_start = payload.get('x_start')
    y_start = payload.get('y_start')
    x_end = payload.get('x_end')
    y_end = payload.get('y_end')

    area = user.user_profile_uploadphoto_area(x_start, y_start, x_end, y_end)
    return dumps(user.user_profile_uploadphoto(token, img_url, area))
