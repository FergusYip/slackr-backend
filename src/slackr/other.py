'''
Functions to provide miscellaneous services to the program. Will allow
users to get a list of all users and search for messages.
'''

from slackr.data_store import DATA_STORE
from slackr.token_validation import decode_token


def users_all(token):
    ''' Returns a list of all users and their associated details

	Parameters:
		token (str): JWT

	Returns (dict):
		users (list): List of users

	'''
    decode_token(token)
    users = DATA_STORE.users_all
    return {'users': users}


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
    user = DATA_STORE.get_user(token_payload['u_id'])
    messages = [
        message.details(user) for message in user.viewable_messages
        if query_str.lower() in message.message.lower()
    ]
    return {'messages': messages}


if __name__ == '__main__':
    pass
