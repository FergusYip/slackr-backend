'''
Implementation of users/all and search routes for slackr app
'''
from data_store import data_store
from token_validation import decode_token
from helpers import user_channels, channel_search


def users_all(token):
    ''' Returns a list of all users and their associated details

	Parameters:
		token (str): JWT

	Returns (dict):
		users (list): List of users

	'''
    decode_token(token)

    users = []
    for user in data_store['users']:
        user_dict = {
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
        }
        users.append(user_dict)

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

    messages = []
    for channel in user_channels(token_payload['u_id']):
        search_results = channel_search(channel, query_str)
        for message in search_results:

            message_reacts = []
            reacts = message['reacts']
            for react in reacts:
                is_this_user_reacted = token_payload['u_id'] in react['u_ids']
                react_info = {
                    'react_id': react['react_id'],
                    'u_ids': react['u_ids'],
                    'is_this_user_reacted': is_this_user_reacted
                }
                message_reacts.append(react_info)

            message_info = {
                'message_id': message['message_id'],
                'u_id': message['u_id'],
                'message': message['message'],
                'time_created': message['time_created'],
                'reacts': message_reacts,
                'is_pinned': message['is_pinned']
            }
            messages.append(message_info)

    return {'messages': messages}


if __name__ == '__main__':
    pass
