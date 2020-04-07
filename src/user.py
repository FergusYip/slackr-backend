'''
Functionality for users of the program to get other user's profile information,
as well as change their own personal information.
'''

from PIL import Image
import requests
from error import InputError
from email_validation import invalid_email
from token_validation import decode_token
from data_store import data_store
import helpers

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

    user_info = helpers.get_user(target_uid)

    if target_uid == -99:
        user_return = data_store['deleted_user_profile']
    elif user_info is None:
        raise InputError(description='User ID is not a valid user')
    else:
        user_return = {
            'u_id': user_info['u_id'],
            'email': user_info['email'],
            'name_first': user_info['name_first'],
            'name_last': user_info['name_last'],
            'handle_str': user_info['handle_str']
        }

    return {'user': user_return}


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
        raise InputError(description='Email address is invalid')

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

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Function that will take a desired url and will resize this image to specific constraints,
    and upload this file to a path in the directory.
    '''

    token_info = decode_token(token)
    user_id = token_info['u_id']

    req = requests.get(f'{img_url}')
    if req.status_code != 200:
        raise InputError(
            description='Image does not exist')

    if helpers.get_image_byte_size(img_url) > 10000000:
        raise InputError(
            description='Image must not be over 10MB')

    url = requests.get(img_url, stream=True)
    img = Image.open(url.raw)

    width, height = img.size

    if x_start > width or x_end > width:
        raise InputError(
            description='Crop constraints are outside of the image')

    if y_start > height or y_end > height:
        raise InputError(
            description='Crop constraints are outside of the image')

    if not img_url.endswith('.jpg'):
        raise InputError(
            description='Image must be a .jpg file')

    area = (x_start, y_start, x_end, y_end)

    region = img.crop(area)

    region.save(f'src/profile_images/{user_id}.jpg')

    return {}


if __name__ == '__main__':
    pass
