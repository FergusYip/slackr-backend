'''
Functions to provide authorisation to the program. Will allow users to
register, login, logout, and reset their password.
'''

import smtplib
from email.message import EmailMessage
from slackr.error import InputError
from slackr.email_validation import invalid_email
from slackr.token_validation import decode_token, encode_token
from slackr import helpers
from slackr import db
from slackr.models import User, ExpiredToken
from slackr.utils.constants import PERMISSIONS
import math


def auth_register(email, password, name_first, name_last):
    ''' Registers a new user

	Parameters:
		email (str): Email of new user
		password (str): Password of new user
		name_first (str): First name of new user
		name_last (str): Last name of new user

	Returns (dict):
		u_id (int): User ID
		token (str): JWT
	'''

    if None in {email, password, name_first, name_last}:
        raise InputError(
            description=
            'Insufficient parameters. Requires email, password, name_first, name_last.'
        )

    if len(password) < 6:
        raise InputError(
            description='Password entered is less than 6 characters long')

    if not 1 <= len(name_first) <= 50:
        raise InputError(
            description=
            'First name is not between 1 and 50 characters inclusive')

    if not 1 <= len(name_last) <= 50:
        raise InputError(
            description='Last name is not between 1 and 50 characters inclusive'
        )

    if invalid_email(email):
        raise InputError(description='Email entered is not a valid email ')

    if User.query.filter_by(email=email).first() is not None:
        raise InputError(
            description='Email address is already being used by another user')

    handle = generate_handle(name_first, name_last)
    user = User(email, password, name_first, name_last, handle)

    if len(User.query.all()) == 0:
        user.permission_id = PERMISSIONS['owner']

    db.session.add(user)
    db.session.commit()

    return {
        'u_id': user.u_id,
        'token': encode_token(user.u_id),
    }


def auth_login(email, password):
    ''' Logs in existing user

	Parameters:
		email (str): Email of user
		password (str): Password of user

	Returns (dict):
		u_id (int): User ID
		token (str): JWT

	'''
    if None in {email, password}:
        raise InputError(
            description='Insufficient parameters. Requires email and password.'
        )

    user = User.query.filter_by(email=email).first()

    if invalid_email(email):
        raise InputError(description='Email entered is not a valid email ')

    if not user:
        raise InputError(description='Email entered does not belong to a user')

    if user.password != helpers.hash_pw(password):
        raise InputError(description='Password is not correct')

    return {'u_id': user.u_id, 'token': encode_token(user.u_id)}


def auth_logout(token):
    ''' Logs out user

	Parameters:
		token (str): JWT of session

	Returns (dict):
		is_success (bool): Whether the user has been logged out

	'''
    if token is None:
        raise InputError(
            description='Insufficient parameters. Requires token.')

    decode_token(token)

    db.session.add(ExpiredToken(token))

    is_success = ExpiredToken.query.filter_by(token=token).first() is not None

    return {'is_success': is_success}


def auth_passwordreset_request(email):
    ''' Makes a password reset request and sends a email to the desired email

    Parameters:
        email (str): Email associated to the account the user wants to reset

    Returns:
        Empty Dictionary
    '''

    # if email is None:
    #     raise InputError(description='Insufficient parameters')

    # user = DATA_STORE.get_user(email=email)

    # DATA_STORE.invalidate_reset_request_from_user(user)

    # reset_code = DATA_STORE.make_reset_request(user)

    # if user is not None:
    #     email_reset_code(email, reset_code)

    return {}


def auth_passwordreset_reset(reset_code, new_password):
    '''Given a reset_code, check that its valid and reset the user's password

        Parameters:
            reset_node (str): Reset code
            new_password (str): Desired new passowrd

        Returns:
            Empty Dictionary
    '''

    # if None in {reset_code, new_password}:
    #     raise InputError(description='Insufficient parameters')

    # reset_code = int(reset_code)
    # reset_request = DATA_STORE.get_reset_request(reset_code)

    # if reset_request is None:
    #     raise InputError(description='Reset code is not valid')

    # if len(new_password) < 6:
    #     raise InputError(description='Password is not valid')

    # user = DATA_STORE.get_user(u_id=reset_request['u_id'])
    # user.set_password(new_password)

    return {}


def email_reset_code(email, reset_code):
    '''Send a email containing a reset code to the provided email

    Parameters:
        email (str): Email
        reset_code (int): Reset code

    Return:
        (bool): Whether the email was sent successfully
    '''
    # sender = None
    # password = None

    # message = EmailMessage()
    # message['Subject'] = 'Slackr: Password Reset Code'
    # message['From'] = sender
    # message['To'] = email
    # message.set_content(f'Your reset code is {reset_code}')

    # message.add_alternative(\
    # f'''
    # <!DOCTPYE html>
    # <html>
    #     <body>
    #         <h1 style="color=Black, align=center">Your password reset code is {reset_code}</h1>
    #     </body>
    # </html>
    # ''', subtype='html')

    # try:
    #     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    #     server.login(sender, password)
    #     server.send_message(message)
    #     server.quit()
    #     print("Successfully sent email")
    #     return True
    # except smtplib.SMTPException:
    #     print("Error: unable to send email")
    #     return False

    return False


def generate_handle(name_first, name_last):
    """ Generate a handle based on name_first and name_last

    Parameters:
        name_first (str): First name
        name_last (str): Last name

    Returns:
        handle_str (str): Unique handle

    """
    # strip all whitespace in the first and last name
    name_first = name_first.replace(' ', '')
    name_last = name_last.replace(' ', '')

    concatentation = name_first.lower() + name_last.lower()
    handle_str = concatentation[:20]

    unique_modifier = 1
    while User.query.filter_by(
            handle_str=handle_str).first() or not handle_str:
        unique_digits = int(math.log10(unique_modifier)) + 1
        handle_str = handle_str[:len(handle_str) - unique_digits]
        handle_str += str(unique_modifier)
        unique_modifier += 1

    return handle_str


if __name__ == '__main__':
    pass
