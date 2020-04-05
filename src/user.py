'''
Functionality for users of the program to get other user's profile information,
as well as change their own personal information.
'''

from error import InputError
from email_validation import invalid_email
from token_validation import decode_token
from data_store import data_store


def user_profile(token, u_id):
    '''
    Function that will return the profile information of a desired
    user on the Slackr platform.
    '''

    # By calling the decode function, multiple error checks are performed.
    decode_token(token)

    u_id = int(u_id)
    target_user = data_store.get_user(u_id)

    if target_user is None:
        raise InputError(description='User ID is not a valid user')

    return {'user': target_user.profile}


def user_profile_setname(token, name_first, name_last):
    '''
    Function that will take a desired first and last name and will change
    the authorized user's information to be updated with this information.
    '''

    token_info = decode_token(token)
    u_id = token_info['u_id']
    user = data_store.get_user(u_id)

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
    '''

    token_info = decode_token(token)
    u_id = token_info['u_id']

    user = data_store.get_user(u_id)

    if email == user.email:
        # To stop an error occurring when the user either types their current
        # email address, or accidently presses the edit button. Assists with
        # a greater user experience.
        return {}

    if invalid_email(email):
        raise InputError(description='Email address is invalid')

    if data_store.get_user(email=email) is not None:
        raise InputError(
            description='Email address is already being used by another user')

    user.set_email(email)

    return {}


def user_profile_sethandle(token, handle_str):
    '''
    Function that will take a desired handle and will change the authorized
    user's information to reflect this new handle.
    '''

    token_info = decode_token(token)
    u_id = token_info['u_id']

    user = data_store.get_user(u_id)

    if handle_str == user.handle_str:
        # To stop an error occurring when the user either types their current
        # handle, or accidently presses the edit button. Assists with a greater
        # user experience.
        return {}

    if not 2 <= len(handle_str) <= 20:
        raise InputError(
            description='Handle is not between 2 and 20 characters')

    if data_store.get_user(handle_str=handle_str):
        raise InputError(
            description='Handle is already being used by another user')

    user.set_handle(handle_str)

    return {}


if __name__ == '__main__':
    pass
