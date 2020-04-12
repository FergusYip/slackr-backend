'''
Implementation of auth routes for slackr app
'''
import math
import smtplib
import random
from email.message import EmailMessage
from error import InputError
from email_validation import invalid_email
from data_store import DATA_STORE as data_store
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

    if invalid_password(password):
        raise InputError(
            description='Password entered is less than 6 characters long')

    if not helpers.user_check_name(name_first):
        raise InputError(
            description=
            'First name is not between 1 and 50 characters inclusive')

    if not helpers.user_check_name(name_last):
        raise InputError(
            description='Last name is not between 1 and 50 characters inclusive'
        )

    if invalid_email(email):
        raise InputError(description='Email entered is not a valid email ')

    if helpers.get_user(email=email) is not None:
        raise InputError(
            description='Email address is already being used by another user')

    u_id = helpers.generate_u_id()
    user = {
        'u_id': u_id,
        'email': email,
        'password': helpers.hash_pw(password),
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': generate_handle(name_first, name_last),
        'permission_id': default_permission(),
        'profile_img_url': 'https://imgur.com/o6OHqnt'
    }

    data_store['users'].append(user)

    return {
        'u_id': u_id,
        'token': encode_token(u_id),
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

    user = helpers.get_user(email=email)

    if invalid_email(email):
        raise InputError(description='Email entered is not a valid email ')

    if not user:
        raise InputError(description='Email entered does not belong to a user')

    if user['password'] != helpers.hash_pw(password):
        raise InputError(description='Password is not correct')

    return {'u_id': user['u_id'], 'token': encode_token(user['u_id'])}


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
    data_store['token_blacklist'].append(token)

    is_success = False

    if token in data_store['token_blacklist']:
        is_success = True

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

    user = helpers.get_user(email=email)
    u_id = user['u_id']

    reset_code = generate_reset_code()

    helpers.invalidate_reset_request_from_user(u_id)

    helpers.make_reset_request(reset_code, u_id)

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

    user = helpers.get_user(email=email)
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
    if None in {reset_code, new_password}:
        raise InputError(description='Insufficient parameters')

    reset_code = int(reset_code)
    reset_request = helpers.get_reset_request(reset_code)

    if reset_request is None:
        raise InputError(description='Reset code is not valid')

    if invalid_password(new_password):
        raise InputError(description='Password is not valid')

    helpers.change_password(reset_request['u_id'], new_password)

    return {}


def invalid_password(password):
    ''' Checks whether a password is invalid

	Parameters:
		password (str): Password

	Returns:
		(bool): Whether the password is invalid

	'''
    if len(password) < 6:
        return True
    return False


def default_permission():
    ''' Returns permission level depending on whether there are registered users

	Returns:
		permission_id (int): ID of permission level

	'''
    if not data_store['users']:
        return data_store['permissions']['owner']
    return data_store['permissions']['member']


def generate_handle(name_first, name_last):
    ''' Generate a handle best on name_first and name_last

	Parameters:
		name_first (str): First name
		name_last (str): Last name

	Returns:
		handle_str (str): Unique handle

	'''
    concatentation = name_first.lower() + name_last.lower()
    handle_str = concatentation[:20]

    unique_modifier = 1
    while helpers.is_handle_used(handle_str):
        split_handle = list(handle_str)

        # Remove n number of characters from split_handle
        unique_digits = int(math.log10(unique_modifier)) + 1
        for _ in range(unique_digits):
            split_handle.pop()

        split_handle.append(str(unique_modifier))
        handle_str = ''.join(split_handle)

        unique_modifier += 1

    return handle_str


def generate_reset_code():
    '''Generate a unique 6 digit reset code'''
    reset_code = random.randint(100000, 999999)
    active_codes = [
        reset_request['reset_code']
        for reset_request in data_store['reset_requests']
    ]
    while reset_code in active_codes:
        reset_code = random.randint(100000, 999999)

    return reset_code


if __name__ == '__main__':
    pass
