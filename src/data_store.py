''' Data Store for the slackr backend'''
import random
import math
import threading
import pickle
import helpers

SECRET = 'the chunts'


class User:
    '''User Object'''
    def __init__(self, email, password, name_first, name_last):
        self.u_id = DATA_STORE.generate_id('u_id')
        self.email = email
        self.password = helpers.hash_pw(password)
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = generate_handle(name_first, name_last)
        self.permission_id = DATA_STORE.default_permission()
        self.channels = []
        self.messages = []
        self.reacts = []
        self.profile_img_url = default_profile_img()

    def set_email(self, email):
        '''Set the user's email

        Parameters:
            email (str): email

        '''
        self.email = email

    def set_name(self, name_first, name_last):
        '''Set the user's firt and last name

        Parameters:
            name_first (str): First name
            name_last (str): Last name

        '''
        self.name_first = name_first
        self.name_last = name_last

    def change_password(self, password):
        '''Change the user's password

        Parameters:
            password (str): Password

        '''
        self.password = helpers.hash_pw(password)

    def set_handle(self, handle_str):
        '''Set the user's handle

        Parameters:
            handle_str (str): Handle String

        '''
        self.handle_str = handle_str

    def change_permission(self, permission_id):
        '''Change the user's permission ID

        Parameters:
            permission_id (int): Permission ID

        '''
        self.permission_id = permission_id

    @property
    def profile(self):
        '''Get a dictionary of the user's profile

        Returns (dict):
            u_id (int): User ID
            email (str): Email
            name_first (str): First name
            name_last (str): Last name
            handle_strd (str): Handle
            profile_img_url (str): Url of profile image

        '''
        return {
            'u_id': self.u_id,
            'email': self.email,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'handle_str': self.handle_str,
            'profile_img_url': self.profile_img_url
        }

    @property
    def details(self):
        '''Get a dictionary of the user's details

        Returns (dict):
            name_first (str): First name
            name_last (str): Last name
            handle_strd (str): Handle
            profile_img_url (str): Url of profile image

        '''
        return {
            'u_id': self.u_id,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'profile_img_url': self.profile_img_url
        }

    def add_channel(self, channel):
        '''Add the user to a channel

        Parameters:
            channel (obj): Channel object

        '''
        self.channels.append(channel)

    def remove_channel(self, channel):
        '''Remove the user to a channel

        Parameters:
            channel (obj): Channel object

        '''
        self.channels.remove(channel)

    def add_message(self, message):
        '''Add a message associated to the user

        Parameters:
            message (obj): Message object

        '''
        self.messages.append(message)

    def remove_message(self, message):
        '''Remove a message associated to the user

        Parameters:
            message (obj): Message object

        '''
        self.messages.remove(message)

    @property
    def viewable_messages(self):
        '''Get a list of all messages viewable to the user

        Returns (list):
            message (obj): Message object

        '''
        msgs = []
        for channel in self.channels:
            for message in channel.messages:
                msgs.append(message)
        return msgs

    def add_react(self, react):
        '''Add a react associated to the user

        Parameters:
            react (obj): React object

        '''
        self.reacts.append(react)

    def remove_react(self, react):
        '''Remove a react associated to the user

        Parameters:
            react (obj): React object

        '''
        self.reacts.remove(react)

    def change_profile_img_url(self, profile_img_url):
        '''Change the user's profile image url

        Parameters:
            profile_img_url (str): Url of profile image

        '''
        self.profile_img_url = profile_img_url


class Standup:
    def __init__(self):
        self.is_active = False
        self.starting_user = None
        self.time_finish = None
        self.messages = []

    def start(self, user, time_finish):
        self.is_active = True
        self.starting_user = user
        self.time_finish = time_finish

    def stop(self):
        joined_message = ''
        for message in self.messages:
            joined_message += f"{message['handle_str']}: {message['message']}\n"

        self.is_active = False
        self.starting_user = None
        self.time_finish = None
        self.messages = []

        return joined_message

    def send(self, user, message):
        message_dict = {'handle_str': user.handle_str, 'message': message}
        self.messages.append(message_dict)


class Channel:
    def __init__(self, creator, name, is_public):
        self.channel_id = DATA_STORE.generate_id('channel_id')
        self.name = name
        self.is_public = is_public
        self.owner_members = [creator]
        self.all_members = [creator]
        self.messages = []
        self.standup = Standup()

    def add_owner(self, user):
        self.owner_members.append(user)

    def remove_owner(self, user):
        self.owner_members.remove(user)

    def add_member(self, user):
        self.all_members.append(user)

    def remove_member(self, user):
        self.all_members.remove(user)

    def is_member(self, user):
        return user in self.all_members

    @property
    def id_name(self):
        return {'channel_id': self.channel_id, 'name': self.name}

    @property
    def details(self):
        return {
            'name': self.name,
            'owner_members': [user.details for user in self.owner_members],
            'all_members': [user.details for user in self.all_members]
        }

    def is_owner(self, user):
        return user in self.owner_members

    def search(self, query_str):
        return [
            message for message in self.messages
            if query_str in message.message
        ]

    def send_message(self, message):
        self.messages.append(message)

    def remove_message(self, message):
        self.messages.remove(message)


class Message:
    def __init__(self, sender, channel, message, message_id=None):
        self.message_id = DATA_STORE.generate_id(
            'message_id') if message_id is None else message_id
        self.sender = sender
        self.channel = channel
        self.message = message
        self.time_created = helpers.utc_now()
        self.reacts = []
        self.is_pinned = False

    @property
    def u_id(self):
        return self.sender.u_id

    def details(self, user):
        message_reacts = []
        reacts = self.reacts
        for react in reacts:
            react_info = {
                'react_id': react.react_id,
                'u_ids': react.u_ids,
                'is_this_user_reacted': react in user.reacts
            }
            message_reacts.append(react_info)

        return {
            'message_id': self.message_id,
            'u_id': self.u_id,
            'message': self.message,
            'time_created': self.time_created,
            'reacts': message_reacts,
            'is_pinned': self.is_pinned
        }

    def pin(self):
        self.is_pinned = True

    def unpin(self):
        self.is_pinned = False

    def get_react(self, react_id):
        for react in self.reacts:
            if react_id == react.react_id:
                return react
        return None

    def add_react(self, react):
        self.reacts.append(react)

    def remove_react(self, react):
        self.reacts.remove(react)


class React:
    def __init__(self, react_id, message):
        self.react_id = react_id
        self.users = []
        self.message = message

    def add_user(self, users):
        self.users.append(users)

    def remove_user(self, users):
        self.users.remove(users)

    @property
    def u_ids(self):
        return [user.u_id for user in self.users]

    def is_user_reacted(self, u_id):
        return u_id in self.u_ids


class DeletedUser:
    '''Deleted user object'''
    def __init__(self):
        self.u_id = -99
        self.email = 'deleted'
        self.name_first = 'Deleted'
        self.name_last = 'User'
        self.handle_str = 'deleted'
        self.profile_img_url = 'https://i.imgur.com/nsoGP2n.jpg'

    @property
    def profile(self):
        '''Return the profile of a deleted user'''
        return {
            'u_id': self.u_id,
            'email': self.email,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'handle_str': self.handle_str,
            'profile_img_url': self.profile_img_url
        }


class HangmanBot:
    '''Hangman bot user object'''
    def __init__(self):
        self.u_id = -95
        self.email = 'hangmanbot'
        self.name_first = 'Hangman'
        self.name_last = 'Bot'
        self.handle_str = 'hangman_bot'
        self.profile_img_url = 'https://i.imgur.com/olQfW6w.jpg'
        self.messages = []

    @property
    def profile(self):
        '''Return the profile of a hangman bot'''
        return {
            'u_id': self.u_id,
            'email': self.email,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'handle_str': self.handle_str,
            'profile_img_url': self.profile_img_url
        }


class DataStore:
    '''Data Store object for storing slackr related information'''
    def __init__(self):
        self.users = []
        self.channels = []
        self.messages = []
        self.token_blacklist = []
        self.permissions = {'owner': 1, 'member': 2}
        self.reactions = {'thumbs_up': 1}
        self.max_ids = {
            'u_id': 0,
            'channel_id': 0,
            'message_id': 0,
        }
        self.time_created = helpers.utc_now()
        self.preset_profiles = {
            'deleted_user': DeletedUser(),
            'hangman_bot': HangmanBot()
        }
        self.reset_requests = []

    def add_user(self, new_user):
        '''Add a user to the data store'''
        self.users.append(new_user)

    def delete_user(self, user):
        '''Delete a user from the data store'''
        for channel in self.channels:
            for owner in channel.owner_members:
                if owner == user:
                    channel.all_members.remove(owner)
                    break
            for member in channel.all_members:
                if member == user:
                    channel.all_members.remove(member)
                    break
        for message in self.messages:
            if message.sender == user:
                message.sender = self.preset_profiles['deleted_user']
        target_user = self.get_user(user.u_id)
        self.users.remove(target_user)

    def add_channel(self, new_channel):
        '''Add a channel to the data store'''
        self.channels.append(new_channel)

    def send_message(self, user, channel, message):
        '''Send a message in the data store'''
        self.messages.append(message)
        user.add_message(message)
        channel.add_message(message)
        message.user = user
        message.channel = channel

    def add_message(self, message):
        '''Add a message in the data store'''
        self.messages.append(message)

    def remove_message(self, message):
        '''Remove a message in the data store'''
        self.messages.remove(message)

    def join_channel(self, user, channel):
        '''Make a user join a channel in the data store'''
        user.channels.append(channel)
        channel.all_members.append(user)

    def get_user(self, u_id=None, email=None, handle_str=None):
        '''Get a user from the data store'''
        if u_id == self.preset_profiles['deleted_user'].u_id:
            return self.preset_profiles['deleted_user']

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

    @property
    def permission_values(self):
        '''Get a list of permission values from the data store'''
        return self.permissions.values()

    def default_permission(self):
        '''Get a default permission_id from data store depending on the number of users'''
        if len(self.users) == 0:
            return self.permissions['owner']
        return self.permissions['member']

    def is_admin(self, user):
        '''Check if a user is an admin'''
        return user.permission_id == DATA_STORE.permissions['owner']

    @property
    def all_admins(self):
        '''Get a list of all admins'''
        return [
            user for user in self.users
            if user.permission_id == DATA_STORE.permissions['owner']
        ]

    def is_admin_or_owner(self, user, channel):
        '''Check if a user is an admin or the owner of the channel'''
        return user.permission_id == DATA_STORE.permissions[
            'owner'] or user in channel.owner_members

    def add_to_blacklist(self, token):
        '''Add a token to the data store blacklist'''
        self.token_blacklist.append(token)

    def generate_id(self, id_type):
        '''Generate an id of id_type'''
        self.max_ids[id_type] += 1
        return self.max_ids[id_type]

    def reset(self):
        '''Reset the data store'''
        self.users.clear()
        self.channels.clear()
        self.messages.clear()
        self.token_blacklist.clear()
        self.reset_requests.clear()

        for key in self.max_ids:
            self.max_ids[key] = 0

        self.time_created = helpers.utc_now()

    def generate_reset_code(self):
        '''Generate a unique 6 digit reset code'''
        reset_code = random.randint(100000, 999999)
        active_codes = [
            reset_request['reset_code']
            for reset_request in self.reset_requests
        ]
        while reset_code in active_codes:
            reset_code = random.randint(100000, 999999)

        return reset_code

    def make_reset_request(self, user):
        ''' Make a reset_request

        Parameters:
            reset_code (int): Reset code
            u_id (int): Requested user

        '''
        reset_code = self.generate_reset_code()
        reset_request = {'reset_code': reset_code, 'u_id': user.u_id}
        self.reset_requests.append(reset_request)
        return reset_code

    def get_reset_request(self, reset_code):
        ''' Given a reset_code, get the associated request

        Parameters:
            reset_code (int): Reset code

        Returns (dict):
            reset_code (int): Reset code
            u_id (int): Requested user
        '''
        for request in self.reset_requests:
            if request['reset_code'] == reset_code:
                return request
        return None

    def invalidate_reset_request(self, reset_code):
        ''' Invalidate a reset_request

        Parameters:
            reset_code (int): Reset code

        '''
        for request in self.reset_requests:
            if request['reset_code'] == reset_code:
                self.reset_requests.remove(request)

    def invalidate_reset_request_from_user(self, user):
        ''' Invalidates all reset requests made by a user

        Parameters:
            u_id (int): User ID

        '''
        for request in self.reset_requests:
            if request['u_id'] == user.u_id:
                self.reset_requests.remove(request)


try:
    DATA_STORE = pickle.load(open('data_store.p', 'rb'))
except FileNotFoundError:
    DATA_STORE = DataStore()


def save():
    '''Save the state of the data_store into a pickle'''
    pickle.dump(DATA_STORE, open('data_store.p', 'wb'))


def autosave():
    '''Thread to save state every second'''
    timer = threading.Timer(1.0, autosave)
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
    concatentation = name_first.lower() + name_last.lower()
    handle_str = concatentation[:20]

    unique_modifier = 1
    while DATA_STORE.get_user(handle_str=handle_str):
        split_handle = list(handle_str)

        # Remove n number of characters from split_handle
        unique_digits = int(math.log10(unique_modifier)) + 1
        for _ in range(unique_digits):
            split_handle.pop()

        split_handle.append(str(unique_modifier))
        handle_str = ''.join(split_handle)

        unique_modifier += 1

    return handle_str


def default_profile_img():
    ''' Return a link to a randomised default image'''
    colors = {
        'blue': 'https://i.imgur.com/HrDzaJo.jpg',
        'green': 'https://i.imgur.com/jETb01M.jpg',
        'purple': 'https://i.imgur.com/qmX0dIZ.jpg',
        'red': 'https://i.imgur.com/FTKy1XA.jpg'
    }
    return random.choice(list(colors.values()))
