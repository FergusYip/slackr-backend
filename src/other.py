'''
Implementation of users/all and search routes for slackr app
'''
from data_store import data_store
from token_validation import decode_token


def users_all(token):
    ''' Returns a list of all users and their associated details

	Parameters:
		token (str): JWT

	Returns (dict):
		users (list): List of users

	'''
    decode_token(token)
    users = data_store.users_all
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
    user = data_store.get_user(token_payload['u_id'])
    messages = [[message.details for message in channel.search(query_str)]
                for channel in user.channels]
    return {'messages': messages}


if __name__ == '__main__':
    pass
