'''
Functions to provide miscellaneous services to the program. Will allow
users to get a list of all users and search for messages.
'''

from slackr.token_validation import decode_token
from slackr.models.user import User
from slackr.utils.constants import RESERVED_UID


def users_all(token):
    ''' Returns a list of all users and their associated details

	Parameters:
		token (str): JWT

	Returns (dict):
		users (list): List of users

	'''
    decode_token(token)
    return {
        'users': [
            user.profile for user in User.query.all()
            if user.u_id not in RESERVED_UID.values()
        ]
    }


def search(token, query_str):
    ''' Return a list of messages in all of the authorised channels that match
        the query

	Parameters:
		token (str): JWT
		query_str (str): Query string

	Returns (dict):
		messages (list): List of messages containing the query string

	'''
    token_payload = decode_token(token)
    user = User.query.get(token_payload['u_id'])
    messages = []
    for channel in user.channels:
        for message in channel.messages:
            if query_str.lower() in message.message.lower():
                messages.append(message.details(user))
    return {'messages': messages}


if __name__ == '__main__':
    pass
