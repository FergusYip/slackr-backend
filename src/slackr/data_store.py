'''
Data store for the slackr backend
'''
import random
import math
import threading
import pickle
from slackr import helpers

SECRET = 'secret'
PORT = 8080


class User:
    ''' User Object '''
    def __init__(self, email, password, name_first, name_last):
        self._u_id = DATA_STORE.generate_id('u_id')
        self._email = email
        self._password = helpers.hash_pw(password)
        self._name_first = name_first
        self._name_last = name_last
        self._handle_str = generate_handle(name_first, name_last)
        self._permission_id = DATA_STORE.default_permission()
        self._channels = []
        self._messages = []
        self._reacts = []
        self._profile_img_url = helpers.default_profile_img()

    @property
    def u_id(self):
        ''' User ID (int) '''
        return self._u_id

    @property
    def email(self):
        ''' User email (str) '''
        return self._email

    @property
    def password(self):
        ''' User password (str) '''
        return self._password

    @property
    def name_first(self):
        ''' User's first name (str) '''
        return self._name_first

    @property
    def name_last(self):
        ''' User's last name (str) '''
        return self._name_last

    @property
    def handle_str(self):
        ''' User's handle (str) '''
        return self._handle_str

    def set_email(self, email):
        ''' Set the user's email

        Parameters:
            email (str): email

        '''
        self._email = email

    def set_name(self, name_first, name_last):
        ''' Set the user's first and last name

        Parameters:
            name_first (str): First name
            name_last (str): Last name

        '''
        self._name_first = name_first
        self._name_last = name_last

    def set_password(self, password):
        ''' Change the user's password

        Parameters:
            password (str): Password

        '''
        self._password = helpers.hash_pw(password)

    def set_handle_str(self, handle_str):
        ''' Set the user's handle

        Parameters:
            handle_str (str): Handle String

        '''
        self._handle_str = handle_str

    @property
    def permission_id(self):
        ''' User's permission ID (int) '''
        return self._permission_id

    def set_permission_id(self, permission_id):
        ''' Change the user's permission ID

        Parameters:
            permission_id (int): Permission ID

        '''
        self._permission_id = permission_id

    @property
    def channels(self):
        ''' User's channels (list[channel_obj])'''
        return list(self._channels)

    @property
    def messages(self):
        ''' User's messages (list[message_obj]) '''
        return list(self._messages)

    @property
    def reacts(self):
        ''' User's reacts (list[react_obj]) '''
        return list(self._reacts)

    @property
    def profile(self):
        ''' Get a dictionary of the user's profile

        Returns (dict):
            u_id (int): User ID
            email (str): Email
            name_first (str): First name
            name_last (str): Last name
            handle_str (str): Handle
            profile_img_url (str): Url of profile image

        '''
        return {
            'u_id': self._u_id,
            'email': self._email,
            'name_first': self._name_first,
            'name_last': self._name_last,
            'handle_str': self._handle_str,
            'profile_img_url': self._profile_img_url
        }

    @property
    def details(self):
        ''' Get a dictionary of the user's details

        Returns (dict):
            name_first (str): First name
            name_last (str): Last name
            handle_str (str): Handle
            profile_img_url (str): Url of profile image

        '''
        return {
            'u_id': self._u_id,
            'name_first': self._name_first,
            'name_last': self._name_last,
            'profile_img_url': self._profile_img_url
        }

    def add_channel(self, channel):
        ''' Add the user to a channel

        Parameters:
            channel (obj): Channel object

        '''
        self._channels.append(channel)

    def remove_channel(self, channel):
        ''' Remove the user to a channel

        Parameters:
            channel (obj): Channel object

        '''
        self._channels.remove(channel)

    def add_message(self, message):
        ''' Add a message associated to the user

        Parameters:
            message (obj): Message object

        '''
        self._messages.append(message)

    def remove_message(self, message):
        ''' Remove a message associated to the user

        Parameters:
            message (obj): Message object

        '''
        self._messages.remove(message)

    @property
    def viewable_messages(self):
        ''' Get a list of all messages viewable to the user

        Returns (list):
            message (obj): Message object

        '''
        msgs = []
        for channel in self._channels:
            for message in channel.messages:
                msgs.append(message)
        return list(msgs)

    def add_react(self, react):
        ''' Add a react associated to the user

        Parameters:
            react (obj): React object

        '''
        self._reacts.append(react)

    def remove_react(self, react):
        ''' Remove a react associated to the user

        Parameters:
            react (obj): React object

        '''
        self._reacts.remove(react)

    @property
    def profile_img_url(self):
        ''' Change the user's profile image url

        Parameters:
            profile_img_url (str): Url of profile image

        '''
        return self._profile_img_url

    def set_profile_img_url(self, profile_img_url):
        ''' Change the user's profile image url

        Parameters:
            profile_img_url (str): Url of profile image

        '''
        self._profile_img_url = profile_img_url


class DeletedUser(User):
    ''' Deleted user object '''

    # Disabled pylint warning because we wanted to retain the user methods
    # but have the DeletedUser object have different initial attributes
    def __init__(self):  # pylint: disable=W0231
        self._u_id = -99
        self._email = 'deleted'
        self._name_first = 'Deleted'
        self._name_last = 'User'
        self._handle_str = 'deleted'
        self._profile_img_url = 'https://i.imgur.com/nsoGP2n.jpg'


class HangmanBot(User):
    ''' Hangman bot user object '''

    # Pylint reasoning same as DeletedUser
    def __init__(self):  # pylint: disable=W0231
        self._u_id = -95
        self._email = 'hangmanbot'
        self._name_first = 'Hangman'
        self._name_last = 'Bot'
        self._handle_str = 'hangman_bot'
        self._profile_img_url = 'https://i.imgur.com/olQfW6w.jpg'
        self._messages = []
        self._token = None

    @property
    def token(self):
        ''' Get the token of the user. (str) '''
        return self._token

    def set_token(self, token):
        ''' Setting the token for the HangmanBot class with a given token. '''
        self._token = token


class Standup:
    ''' Standup Object '''
    def __init__(self):
        self._is_active = False
        self._starting_user = None
        self._time_finish = None
        self._messages = []

    @property
    def is_active(self):
        ''' Whether the standup is active (bool) '''
        return self._is_active

    @property
    def starting_user(self):
        ''' The user who started the standup (user_obj) '''
        return self._starting_user

    @property
    def time_finish(self):
        ''' Standup end time (int) '''
        return self._time_finish

    @property
    def messages(self):
        ''' Standup messages (list[message_obj]) '''
        return self._messages

    def start(self, user, time_finish):
        ''' Start the standup

        Parameters:
            user (obj): The user who started the standup
            time_finished (int): The desired end time of the standup

        '''
        self._is_active = True
        self._starting_user = user
        self._time_finish = time_finish

    def stop(self):
        ''' Stop the standup

        Parameters:
            user (obj): The user who started the standup
            time_finished (int): The desired end time of the standup

        Return:
            joined_message (str): Standup summary message (joined string of all
                                  standup messages)

        '''
        joined_message = ''
        for message in self._messages:
            joined_message += f"{message['handle_str']}: {message['message']}\n"

        self._is_active = False
        self._starting_user = None
        self._time_finish = None
        self._messages.clear()

        return joined_message

    def send(self, user, message):
        ''' Send a standup message

        Parameters:
            user (obj): The user who sent the message
            message (str): Message

        '''
        message_dict = {'handle_str': user.handle_str, 'message': message}
        self.messages.append(message_dict)


class Hangman:
    ''' Hangman object. '''
    def __init__(self):
        self.is_active = False
        self.word = None
        self.guesses = set()
        self.incorrect = set()
        self.stage = 0
        self.prev_msg = None

    def start(self):
        ''' Function to start a hangman game.

        Return:
            self.word (str): The word to be guessed.

        '''
        self.is_active = True
        self.word = helpers.get_word()
        return self.word

    def stop(self):
        ''' Function to stop a hangman game. '''
        self.is_active = False
        self.word = None
        self.guesses = set()
        self.incorrect = set()
        self.stage = 0
        self.prev_msg = None

    def guess(self, letter):
        ''' Function to make a guess at the word being played.

        Parameters:
            letter (str): The character to be guessed.

        Return:
            Boolean: Either True if correct guess or False if incorrect.

        '''
        letter = letter.lower()
        self.guesses.add(letter)

        # incorrect guess
        if letter not in self.word.lower():
            if letter not in self.incorrect:
                self.stage += 1
                self.incorrect.add(letter)
            return False

        return True


class Channel:
    ''' Channel object '''
    def __init__(self, creator, name, is_public):
        self._channel_id = DATA_STORE.generate_id('channel_id')
        self._name = name
        self._is_public = is_public
        self._owner_members = [creator]
        self._all_members = [creator]
        self._messages = []
        self._standup = Standup()
        self._hangman = Hangman()

    @property
    def channel_id(self):
        ''' Channel ID (int) '''
        return self._channel_id

    @property
    def name(self):
        ''' Channel name (str) '''
        return self._name

    @property
    def is_public(self):
        ''' Channel public status (bool) '''
        return self._is_public

    @property
    def owner_members(self):
        ''' Channel owners (list[user_obj]) '''
        return list(self._owner_members)

    @property
    def all_members(self):
        ''' Channel members (list[user_obj]) '''
        return list(self._all_members)

    @property
    def messages(self):
        ''' Channel messages (list[message_obj]) '''
        return list(self._messages)

    @property
    def standup(self):
        ''' Channel standup (standup_obj) '''
        return self._standup

    @property
    def hangman(self):
        ''' Channel hangman game (hangman_obj) '''
        return self._hangman

    def add_owner(self, user):
        ''' Add a user to the list of owner members.

        Parameters:
            user (obj): A user object.

        '''
        self._owner_members.append(user)

    def remove_owner(self, user):
        ''' Removes a user from the list of owner members.

        Parameters:
            user (obj): A user object.

        '''
        self._owner_members.remove(user)

    def add_member(self, user):
        ''' Add a user to the list of members.

        Parameters:
            user (obj): A user object.

        '''
        self._all_members.append(user)

    def remove_member(self, user):
        ''' Removes a user from the list of members.

        Parameters:
            user (obj): A user object.

        '''
        self._all_members.remove(user)

    def is_member(self, user):
        ''' Determines if a given user is a member of the channel.

        Parameters:
            user (obj): A user object.

        Return:
            Bool: Whether the user is a member of the channel (True) or not (False).

        '''
        return user in self.all_members

    @property
    def id_name(self):
        ''' Get a dictionary containing channel information.

        Return (dict):
            channel_id (int): The unique identification code of the channel.
            name (str): The name of the channel.

        '''
        return {'channel_id': self.channel_id, 'name': self.name}

    @property
    def details(self):
        ''' Get a dictionary containing information within the channel.

        Return (dict):
            name (str): The name of the channel.
            owner_members (list):
                u_id (int): The user's ID.
            all_members (list):
                u_id (int): The user's ID.

        '''
        return {
            'name': self.name,
            'owner_members': [user.details for user in self.owner_members],
            'all_members': [user.details for user in self.all_members]
        }

    def is_owner(self, user):
        ''' Determines whether a user is an owner member.

        Parameters:
            user (obj): A user object.

        Return:
            Bool: Whether the user is an owner (True) or not (False).

        '''
        return user in self.owner_members

    def search(self, query_str):
        ''' Return a list of messages containing the provided query_str

        Parameters:
            query_str (str): Query string

        Return (list):
            message (obj): A message object.

        '''
        return [
            message for message in self.messages
            if query_str in message.message
        ]

    def send_message(self, message):
        ''' Send a message in the channel

        Parameters:
            message (obj): A message object

        '''
        self._messages.append(message)

    def remove_message(self, message):
        ''' Remove a message from the channel

        Parameters:
            message (obj): A message object

        '''
        self._messages.remove(message)


class Message:
    ''' Message object '''
    def __init__(self, sender, channel, message, message_id=None):
        self._message_id = DATA_STORE.generate_id(
            'message_id') if message_id is None else message_id
        self._sender = sender
        self._channel = channel
        self._message = message
        self._time_created = helpers.utc_now()
        self._reacts = []
        self._is_pinned = False

    @property
    def u_id(self):
        ''' Sender's u_id (int) '''
        return self._sender.u_id

    @property
    def sender(self):
        ''' Sender of the message (user_obj) '''
        return self._sender

    @property
    def message_id(self):
        ''' The message's message_id (int) '''
        return self._message_id

    @property
    def channel(self):
        ''' Channel the message was posted in (channel_obj) '''
        return self._channel

    @property
    def message(self):
        ''' The contents of the message. (str) '''
        return self._message

    @property
    def time_created(self):
        ''' Unix timestamp of when the message was sent. (int) '''
        return self._time_created

    @property
    def reacts(self):
        ''' List of all reacts on the message. (list[react_obj]) '''
        return self._reacts

    @property
    def is_pinned(self):
        ''' The message's pinned status. (bool) '''
        return self._is_pinned

    def details(self, user):
        ''' Get a dictionary of the message's information.

        Parameters:
            user (obj): An object of a user.

        Returns (dict):
            message_id (int): The message's unique identification number.
            u_id (int): The user who sent the message's u_id.
            message (str): The contents of the message to be sent.
            time_created (int): A unix timestamp of when the message was sent.
            reacts (list):
                react_id (int): The ID of the reaction denoting which type of reaction it is.
                u_ids (list):
                    u_id (int): The u_id of the users who have made this specific reaction.
                is_this_user_reacted (bool): Whether the user has reacted to the message.
            is_pinned (bool):  Whether the message has been pinned.

        '''
        return {
            'message_id': self.message_id,
            'u_id': self.u_id,
            'message': self.message,
            'time_created': self.time_created,
            'reacts': [react.details(user) for react in self.reacts],
            'is_pinned': self.is_pinned
        }

    def set_sender(self, sender):
        ''' Set the sender of the message with a user object '''
        self._sender = sender

    def set_channel(self, channel):
        ''' Set the channel the message was posted within with a channel object. '''
        self._channel = channel

    def edit(self, new_message):
        ''' Edit the message object with a new string. '''
        self._message = new_message

    def pin(self):
        ''' Set a message to be pinned. '''
        self._is_pinned = True

    def unpin(self):
        ''' Set a message to be unpinned. '''
        self._is_pinned = False

    def get_react(self, react_id):
        ''' Return a react object attached to a message.

        Parameters:
            react_id (int): React ID as an integer.

        Returns:
            react (obj): A react object.

        '''
        for react in self._reacts:
            if react_id == react.react_id:
                return react
        return None

    def add_react(self, react):
        ''' Append a react object to the message. '''
        self._reacts.append(react)

    def remove_react(self, react):
        ''' Remove a react object from the message. '''
        self._reacts.remove(react)


class React:
    ''' React object '''
    def __init__(self, react_id, message):
        self._react_id = react_id
        self._users = []
        self._message = message

    @property
    def react_id(self):
        ''' The ID of the reaction. (int) '''
        return self._react_id

    @property
    def users(self):
        ''' User objects that have used this reaction. (list[user_obj])'''
        return list(self._users)

    @property
    def u_ids(self):
        ''' User IDs that have used this reaction. (list[int])'''
        return [user.u_id for user in self._users]

    @property
    def message(self):
        ''' The message object that the react is attached to. (message_obj) '''
        return self._message

    def details(self, user):
        ''' Details about the reaction from a given user's perspective.

        Parameters:
            user (obj): A user object.

        Return (dict):
            react_id (int): The ID of the reaction.
            u_ids (list):
                u_id (int): The u_id of a user who has reacted.
            is_this_user_reacted (bool): Whether the user has reacted or not.

        '''
        return {
            'react_id': self.react_id,
            'u_ids': self.u_ids,
            'is_this_user_reacted': self in user.reacts
        }

    def add_user(self, user):
        ''' Adds a given user object to the list of users who have reacted. '''
        self._users.append(user)

    def remove_user(self, user):
        ''' Removes a given user object from the list of users who have reacted. '''
        self._users.remove(user)

    def is_user_reacted(self, u_id):
        ''' Checks if a u_id is in the list of u_ids that have reacted.

        Parameters:
            u_id (int): The u_id of the user.

        Return:
            Bool: Whether the user has reacted (True) or not (False).

        '''
        return u_id in self.u_ids


class DataStore:
    ''' Data Store object for storing slackr related information '''
    def __init__(self):
        self._users = []
        self._channels = []
        self._messages = []
        self._token_blacklist = []
        self._permissions = {'owner': 1, 'member': 2}
        self._reactions = {'thumbs_up': 1}
        self._max_ids = {
            'u_id': 0,
            'channel_id': 0,
            'message_id': 0,
        }
        self._time_created = helpers.utc_now()
        self._preset_profiles = {
            'deleted_user': DeletedUser(),
            'hangman_bot': HangmanBot()
        }
        self._reset_requests = []
        self._img_ids = []

    @property
    def users(self):
        ''' List of users in the data store (list[user_obj]) '''
        return self._users

    @property
    def channels(self):
        ''' List of channels in the data store (list[channel_obj]) '''
        return self._channels

    @property
    def messages(self):
        ''' List of messages in the data store (list[message_obj]) '''
        return self._messages

    @property
    def token_blacklist(self):
        ''' List of blacklisted tokens in the data store (list[str]) '''
        return list(self._token_blacklist)

    @property
    def permissions(self):
        ''' Dictionary of permission types in the data store (dict[int]) '''
        return dict(self._permissions)

    @property
    def reactions(self):
        ''' Dictionary of all reaction types in the data store (dict[int]) '''
        return dict(self._reactions)

    @property
    def max_ids(self):
        ''' Dictionary of the max ID values in the data store (dict[int]) '''
        return dict(self._max_ids)

    @property
    def time_created(self):
        ''' The time the data store was created as a unix timestamp. (int) '''
        return self._time_created

    @property
    def preset_profiles(self):
        ''' Dictionary of the preset profiles for the data store. (dict[user_obj]) '''
        return dict(self._preset_profiles)

    @property
    def reset_requests(self):
        ''' List of reset password requests. (list[dict]) '''
        return list(self._reset_requests)

    @property
    def img_ids(self):
        ''' List of img_ids currently in use. (list[str]) '''
        return list(self._img_ids)

    def add_user(self, new_user):
        ''' Add a given user object to the data store. '''
        self._users.append(new_user)

    def delete_user(self, user):
        '''Delete a user from the data store'''
        for channel in self._channels:
            for owner in channel.owner_members:
                if owner == user:
                    channel.remove_owner(owner)
                    break
            for member in channel.all_members:
                if member == user:
                    channel.remove_member(member)
                    break
        for message in self._messages:
            if message.sender == user:
                message.set_sender(self.preset_profiles['deleted_user'])
        target_user = self.get_user(user.u_id)
        self._users.remove(target_user)

    def add_channel(self, new_channel):
        '''Add a channel to the data store'''
        self.channels.append(new_channel)

    def add_message(self, message):
        '''Add a message in the data store'''
        self.messages.append(message)

    def remove_message(self, message):
        '''Remove a message in the data store'''
        self.messages.remove(message)

    def get_user(self, u_id=None, email=None, handle_str=None):
        '''Get a user from the data store'''
        if u_id == self.preset_profiles['deleted_user'].u_id:
            return self.preset_profiles['deleted_user']

        if u_id == self.preset_profiles['hangman_bot'].u_id:
            return self.preset_profiles['hangman_bot']

        for user in self.users:
            if u_id == user.u_id or email == user.email or handle_str == user.handle_str:
                return user
        return None

    @property
    def u_ids(self):
        '''Get a list of all u_ids in the data store'''
        return [user.u_id for user in self.users]

    @property
    def users_all(self):
        '''Get a list of all user profiles in the data store'''
        return [user.profile for user in self.users]

    def get_channel(self, channel_id):
        '''Get a channel from the data store'''
        for channel in self.channels:
            if channel_id == channel.channel_id:
                return channel
        return None

    def user_channels(self, u_id):
        '''Retrieve a list of a user's joined channels'''
        return [
            channel for channel in self.channels if u_id in channel.all_members
        ]

    def get_message(self, message_id):
        '''Get a message from the data store'''
        for message in self.messages:
            if message_id == message.message_id:
                return message
        return None

    def default_permission(self):
        '''Get a default permission_id from data store depending on the number of users'''
        if not self.users:
            return self.permissions['owner']
        return self.permissions['member']

    def is_admin(self, user):
        '''Check if a user is an admin'''
        return user.permission_id == self.permissions['owner']

    @property
    def all_admins(self):
        '''Get a list of all admins'''
        return [
            user for user in self.users
            if user.permission_id == DATA_STORE.permissions['owner']
        ]

    def is_admin_or_owner(self, user, channel):
        '''Check if a user is an admin or the owner of the channel'''
        return user.permission_id == self.permissions[
            'owner'] or user in channel.owner_members

    def add_to_blacklist(self, token):
        '''Add a token to the data store blacklist'''
        self._token_blacklist.append(token)

    def generate_id(self, id_type):
        '''Generate an id of id_type'''
        self._max_ids[id_type] += 1
        return self.max_ids[id_type]

    def reset(self):
        '''Reset the data store'''
        self._users.clear()
        self._channels.clear()
        self._messages.clear()
        self._token_blacklist.clear()
        self._reset_requests.clear()
        self._img_ids.clear()

        for key in self._max_ids:
            self._max_ids[key] = 0

        self._time_created = helpers.utc_now()

    def make_reset_request(self, user):
        ''' Make a reset_request

        Parameters:
            reset_code (int): Reset code
            u_id (int): Requested user

        '''
        active_codes = [
            request['reset_code'] for request in self.reset_requests
        ]
        reset_code = helpers.generate_reset_code(active_codes)
        reset_request = {'reset_code': reset_code, 'u_id': user.u_id}
        self._reset_requests.append(reset_request)
        return reset_code

    def get_reset_request(self, reset_code):
        ''' Given a reset_code, get the associated request

        Parameters:
            reset_code (int): Reset code

        Returns (dict):
            reset_code (int): Reset code
            u_id (int): Requested user
        '''
        for request in self._reset_requests:
            if request['reset_code'] == reset_code:
                return request
        return None

    def invalidate_reset_request(self, reset_code):
        ''' Invalidate a reset_request

        Parameters:
            reset_code (int): Reset code

        '''
        for request in self._reset_requests:
            if request['reset_code'] == reset_code:
                self._reset_requests.remove(request)

    def invalidate_reset_request_from_user(self, user):
        ''' Invalidates all reset requests made by a user

        Parameters:
            u_id (int): User ID

        '''
        for request in self._reset_requests:
            if request['u_id'] == user.u_id:
                self._reset_requests.remove(request)

    def add_img_id(self, img_id):
        ''' Add a image url to the data store

        Parameters:
            img_id (str): Image ID
        '''
        self.img_ids.append(img_id)

    def remove_img_id(self, img_id):
        ''' Remove a image url from the data store

        Parameters:
            img_id (str): Image ID
        '''
        self.img_ids.remove(img_id)


try:
    DATA_STORE = pickle.load(open('data_store.p', 'rb'))
except FileNotFoundError:
    DATA_STORE = DataStore()


def save():
    '''Save the state of the data_store into a pickle'''
    pickle.dump(DATA_STORE, open('data_store.p', 'wb'))


def autosave():
    '''Thread to save state every second'''
    timer = threading.Timer(5.0, autosave)
    timer.start()
    save()


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
    while DATA_STORE.get_user(handle_str=handle_str) or not handle_str:
        unique_digits = int(math.log10(unique_modifier)) + 1
        handle_str = handle_str[:len(handle_str) - unique_digits]
        handle_str += str(unique_modifier)
        unique_modifier += 1

    return handle_str


def change_profile_image(img, user):
    ''' Function to change the profile image url of a given user.

    Parameters:
        img (obj): An image object
        user (obj): A user object
    '''
    curr_id = helpers.get_filename(user.profile_img_url).replace('.jpg', '')
    if curr_id in DATA_STORE.img_ids:
        DATA_STORE.remove_img_id(curr_id)

    # Generate a random 15 digit integer.
    img_id = random.randint(10**14, 10**15 - 1)
    while img_id in DATA_STORE.img_ids:
        img_id = random.randint(10**14, 10**15 - 1)

    img.save(f'src/profile_images/{img_id}.jpg')

    DATA_STORE.add_img_id(img_id)

    base_url = f'http://127.0.0.1:{PORT}'
    url = f'{base_url}/imgurl/{img_id}.jpg'
    user.set_profile_img_url(url)


def set_port(port):
    ''' Set the port the server will run on from a given integer. '''
    global PORT  # pylint: disable=W0603
    PORT = port
