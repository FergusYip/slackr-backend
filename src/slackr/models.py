from datetime import datetime
from slackr import db
from slackr import helpers
from slackr.utils.constants import PERMISSIONS


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


user_channel_identifier = db.Table(
    'user_channel_identifier',
    db.Column('u_id', db.Integer, db.ForeignKey('user.u_id')),
    db.Column('channel_id', db.Integer, db.ForeignKey('channel.channel_id')))

owner_channel_identifier = db.Table(
    'owner_channel_identifier',
    db.Column('u_id', db.Integer, db.ForeignKey('user.u_id')),
    db.Column('channel_id', db.Integer, db.ForeignKey('channel.channel_id')))

message_react_identifier = db.Table(
    'message_react_identifier',
    db.Column('message_id', db.Integer, db.ForeignKey('message.message_id')),
    db.Column('react_id', db.Integer, db.ForeignKey('react.react_id')))

user_react_identifier = db.Table(
    'user_react_identifier',
    db.Column('u_id', db.Integer, db.ForeignKey('user.u_id')),
    db.Column('react_id', db.Integer, db.ForeignKey('react.react_id')))


class User(db.Model):
    u_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(250))
    name_first = db.Column(db.String(50))
    name_last = db.Column(db.String(50))
    handle_str = db.Column(db.String(20))
    permission_id = db.Column(db.Integer)
    messages = db.relationship('Message', backref='sender', lazy=True)
    reacts = db.relationship("React", secondary=user_react_identifier)
    profile_img_url = db.Column(db.String(2000))

    def __init__(self, email, password, name_first, name_last, handle):
        self.email = email
        self.password = helpers.hash_pw(password)
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = handle
        self.permission_id = PERMISSIONS['member']
        self.profile_img_url = helpers.default_profile_img()

    def __repr__(self):
        return f'{self.email}: {self.name_first}'

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
            'u_id': self.u_id,
            'email': self.email,
            'name_first': self.name_first,
            'name_last': self.name_last,
            'handle_str': self.handle_str,
            'profile_img_url': self.profile_img_url
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
            'u_id': self.u_id,
            'name_first': self.name_first,
            'name_last': self.name_last,
            # 'profile_img_url': self.profile_img_url
        }


class Channel(db.Model):
    channel_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    is_public = db.Column(db.Boolean)
    owner_members = db.relationship("User",
                                    backref=db.backref('owned_channels',
                                                       lazy=True),
                                    secondary=owner_channel_identifier)
    all_members = db.relationship("User",
                                  backref=db.backref('channels', lazy=True),
                                  secondary=user_channel_identifier)
    messages = db.relationship('Message', backref='channel', lazy=True)
    standup = Standup()

    # hangman = None

    def __init__(self, user, name, is_public):
        self.name = name
        self.is_public = is_public
        self.all_members.append(user)
        self.owner_members.append(user)

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

    def is_member(self, user):
        ''' Determines if a given user is a member of the channel.

        Parameters:
            user (obj): A user object.

        Return:
            Bool: Whether the user is a member of the channel (True) or not (False).

        '''
        return user in self.all_members

    def is_owner(self, user):
        ''' Determines whether a user is an owner member.

        Parameters:
            user (obj): A user object.

        Return:
            Bool: Whether the user is an owner (True) or not (False).

        '''
        return user in self.owner_members

    @property
    def id_name(self):
        ''' Get a dictionary containing channel information.

        Return (dict):
            channel_id (int): The unique identification code of the channel.
            name (str): The name of the channel.

        '''
        return {'channel_id': self.channel_id, 'name': self.name}


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.u_id'), nullable=False)
    channel_id = db.Column(db.Integer,
                           db.ForeignKey('channel.channel_id'),
                           nullable=False)
    message = db.Column(db.String(1000))
    time_created = db.Column(
        db.Integer,
        nullable=False,
    )
    reacts = db.relationship("React", backref="message", lazy=True)
    is_pinned = db.Column(db.Boolean, default=False)
    is_hidden = db.Column(db.Boolean, default=False)

    def __init__(self, message, u_id, channel_id):
        self.message = message
        self.u_id = u_id
        self.channel_id = channel_id
        self.time_created = helpers.utc_now()

    def __repr__(self):
        return f'{self.time_created}: {self.message}'

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

    def get_react(self, react_id):
        ''' Return a react object attached to a message.

        Parameters:
            react_id (int): React ID as an integer.

        Returns:
            react (obj): A react object.

        '''
        for react in self.reacts:
            if react_id == react.react_id:
                return react
        return None


class React(db.Model):
    react_id = db.Column(db.Integer, primary_key=True)
    users = db.relationship("User", secondary=user_react_identifier)
    message_id = db.Column(db.Integer,
                           db.ForeignKey('message.message_id'),
                           nullable=False)

    def __init__(self, react_id):
        self.react_id = react_id

    def __repr__(self):
        return f'{self.message}: {self.react_id}'

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
            'u_ids': [user.u_id for user in self.users],
            'is_this_user_reacted': self in user.reacts
        }


class ExpiredToken(db.Model):
    token_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500))

    def __init__(self, token):
        self.token = token


class ImageID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(15))


db.create_all()