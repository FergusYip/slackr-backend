'''
Functionality for users of the program to get other user's profile information,
as well as change their own personal information.
'''

from PIL import Image
import requests
from error import InputError
from email_validation import invalid_email
from token_validation import decode_token
from data_store import DATA_STORE


def user_profile(token, u_id):
    '''
    Function that will return the profile information of a desired
    user on the Slackr platform.

    Parameters:
        token (str): The token of the authorized user to be decoded to get the u_id.
        target_uid (int): The u_id of the target user.

    Return:
        Dictionary (dict): A dictionary containing values of the u_id, the
                           user's email, the user's first and last name, and
                           the user's handle.
    '''

    # By calling the decode function, multiple error checks are performed.
    decode_token(token)

    u_id = int(u_id)
    target_user = DATA_STORE.get_user(u_id)

    if target_user is None:
        raise InputError(description='User ID is not a valid user')

    return {'user': target_user.profile}


def user_profile_setname(token, name_first, name_last):
    '''
    Function that will take a desired first and last name and will change
    the authorized user's information to be updated with this information.

    Parameters:
        token (str): The token of the authorized user to be decoded to get the u_id.
        first_name (str): The first name that the user wishes to change to.
        last_name (str): The last name that the user wishes to change to.

    Return:
        Dictionary (dict): An empty dictionary.
    '''

    token_info = decode_token(token)
    u_id = token_info['u_id']
    user = DATA_STORE.get_user(u_id)

    if not 1 <= len(name_first) <= 50:
        raise InputError(
            description='First name is not between 1 and 50 characters')

    if not 1 <= len(name_last) <= 50:
        raise InputError(
            description='Last name is not between 1 and 50 characters')

    user.set_name(name_first, name_last)

    return {}


def user_profile_setemail(token, email):
    '''
    Function that will take a desired email and will change
    the authorized user's information to be updated with this information.

    Parameters:
        token (str): The token of the authorized user to be decoded to get the u_id.
        email (str): The email that the user wishes to change to.

    Return:
        Dictionary (dict): An empty dictionary.
    '''

    token_info = decode_token(token)
    u_id = token_info['u_id']

    user = DATA_STORE.get_user(u_id)

    if email == user.email:
        # To stop an error occurring when the user either types their current
        # email address, or accidently presses the edit button. Assists with
        # a greater user experience.
        return {}

    if invalid_email(email):
        raise InputError(description='Email address is invalid')

    if DATA_STORE.get_user(email=email) is not None:
        raise InputError(
            description='Email address is already being used by another user')

    user.set_email(email)

    return {}


def user_profile_sethandle(token, handle_str):
    '''
    Function that will take a desired handle and will change the authorized
    user's information to reflect this new handle.

    Parameters:
        token (str): The token of the authorized user to be decoded to get the u_id.
        handle_str (str): The handle that the user wishes to change to.

    Return:
        Dictionary (dict): An empty dictionary.
    '''

    token_info = decode_token(token)
    u_id = token_info['u_id']

    user = DATA_STORE.get_user(u_id)

    if handle_str == user.handle_str:
        # To stop an error occurring when the user either types their current
        # handle, or accidently presses the edit button. Assists with a greater
        # user experience.
        return {}

    if not 2 <= len(handle_str) <= 20:
        raise InputError(
            description='Handle is not between 2 and 20 characters')

    if DATA_STORE.get_user(handle_str=handle_str):
        raise InputError(
            description='Handle is already being used by another user')

    user.set_handle(handle_str)

    return {}


def user_profile_uploadphoto_area(x_start, y_start, x_end, y_end):
    '''
    Function that will create and return a tuple of the desired area the user wants to crop to.

    Parameters:
        x_start (int): The coordinate of the x starting position.
        y_start (int): The coordinate of the y starting position.
        x_end (int): The coordinate of the ending x position.
        y_end (int): The coordinate of the ending y position.

    Return:
        List (list): A list containing these values.
    '''

    return [x_start, y_start, x_end, y_end]


def user_profile_uploadphoto(token, img_url, area):
    '''
    Function that will take a desired url and will resize this image to specific constraints,
    flip the image where necessary, and upload this file to a path in the directory.

    Parameters:
        token (str): The token of the authorized user to be decoded to get the u_id.
        img_url (str): A string of the image URL to upload.
        area (list): A list containing the x_start, y_start, x_end, y_end values in that order.

    Return:
        Dictionary (dict): An empty dictionary.
    '''

    token_info = decode_token(token)
    user_id = token_info['u_id']
    user = DATA_STORE.get_user(user_id)

    req = requests.get(f'{img_url}')
    if req.status_code != 200:
        raise InputError(description='Image does not exist')

    url = requests.get(img_url, stream=True)
    img = Image.open(url.raw)

    width, height = img.size

    if len(area) != 4:
        raise InputError(
            description='Must provide 4 integers for the cropping')

    if area[0] > width or area[2] > width:
        raise InputError(
            description='Crop constraints are outside of the image')

    if area[1] > height or area[3] > height:
        raise InputError(
            description='Crop constraints are outside of the image')

    if area[0] > area[2]:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        area[0], area[2] = area[2], area[0]

    if area[1] > area[3]:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        area[1], area[3] = area[3], area[1]

    if any(x < 0 for x in area):
        raise InputError(
            description='Cannot crop out of the bounds of the image')

    if not img_url.endswith('.jpg'):
        raise InputError(description='Image must be a .jpg file')

    region = img.crop(area)

    region.save(f'src/profile_images/{user_id}.jpg')

    base_url = 'http://127.0.0.1:8080'
    user.profile_image_url = f'{base_url}/imgurl/{user_id}.jpg'
    # user.change_profile_image_url(f'{base_url}/imgurl/{user_id}.jpg')

    return {}


if __name__ == '__main__':
    pass
