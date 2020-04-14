'''
Implementation of auth routes for slackr app
'''

import smtplib
from email.message import EmailMessage
from error import InputError
from email_validation import invalid_email
from data_store import DATA_STORE, User
from token_validation import decode_token, encode_token
import helpers


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

    if DATA_STORE.get_user(email=email) is not None:
        raise InputError(
            description='Email address is already being used by another user')

    user = User(email, password, name_first, name_last)
    DATA_STORE.add_user(user)
    
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

    user = DATA_STORE.get_user(email=email)

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
    DATA_STORE.add_to_blacklist(token)

    is_success = token in DATA_STORE.token_blacklist

    return {'is_success': is_success}



def auth_passwordreset_request(email):
    ''' Makes a password reset request and sends a email to the desired email

    Parameters:
        email (str): Email assocaited to the account the user wants to reset

    Returns:
        Empty Dictionary
    '''

    if email is None:
        raise InputError(description='Insufficient parameters')

    user = DATA_STORE.get_user(email=email)

    DATA_STORE.invalidate_reset_request_from_user(user)

    reset_code = DATA_STORE.make_reset_request(user)

    sender = 'thechunts.slackr@gmail.com'
    password = 'chuntsslackr'

    message = EmailMessage()
    message['Subject'] = 'Slackr: Password Reset Code'
    message['From'] = sender
    message['To'] = email
    message.set_content(f'Your reset code is {reset_code}')

    message.add_alternative(\
    f'''
    <!DOCTPYE html>
    <html>
        <body>
            <h1 style="color=Black, align=center">Your password reset code is {reset_code}</h1>
        </body>
    </html>
    ''', subtype='html')

    if user is not None:
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender, password)
            server.send_message(message)
            server.quit()
            print("Successfully sent email")
        except smtplib.SMTPException:
            print("Error: unable to send email")

    return {}


def auth_passwordreset_reset(reset_code, new_password):
    '''Given a reset_code, check that its valid and reset the user's password

        Parameters:
            reset_node (str): Reset code
            new_password (str): Desired new passowrd

        Returns:
            Empty Dictionary
    '''

    reset_code = int(reset_code)
    reset_request = DATA_STORE.get_reset_request(reset_code)

    if reset_request is None:
        raise InputError(description='Reset code is not valid')

    if len(new_password) < 6:
        raise InputError(description='Password is not valid')

    user = DATA_STORE.get_user(u_id=reset_request['u_id'])
    user.change_password(new_password)

    return {}

if __name__ == '__main__':
    pass
