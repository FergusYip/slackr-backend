'''
Implementation of users/all and search routes for slackr app
'''
from json import dumps
from flask import request, Blueprint
from data_store import data_store
from token_validation import decode_token

OTHER = Blueprint('other', __name__)


@OTHER.route("/users/all", methods=['GET'])
def route_users_all():
    '''Flask route for /users/all'''
    token = request.values.get('token')
    return dumps(users_all(token))


@OTHER.route("/search", methods=['GET'])
def route_search():
    '''Flask route for /search'''
    token = request.values.get('token')
    query_str = request.values.get('query_str')
    return dumps(search(token, query_str))


def users_all(token):
    """ Returns a list of all users and their associated details

	Parameters:
		token (str): JWT

	Returns (dict):
		users (list): List of users

	"""
    decode_token(token)
    users = data_store.users_all
    return {'users': users}


def search(token, query_str):
    """ Return a list of messages in all of the authorised channels that match
        the query

	Parameters:
		token (str): JWT
		query_str (str): Query string

	Returns (dict):
		messages (list): List of messages containing the query string

	"""
    token_payload = decode_token(token)
    user = data_store.get_user(token_payload['u_id'])
    messages = [[message.details for message in channel.search(query_str)]
                for channel in user.channels]
    return {'messages': messages}


if __name__ == "__main__":
    pass
