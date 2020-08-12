from slackr import db
from slackr import helpers
from slackr.utils.constants import PERMISSIONS

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

    # messages = db.relationship('Message', backref='sender', lazy=True)

    def __init__(self, email, password, name_first, name_last, handle):
        self.email = email
        self.password = helpers.hash_pw(password)
        self.name_first = name_first
        self.name_last = name_last
        self.handle_str = handle
        self.permission_id = PERMISSIONS['member']
        # self.profile_img_url = helpers.default_profile_img()

    def __repr__(self):
        return f'{self.email}: {self.name_first}'


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
    # standup = db.Column(db.Integer)
    # hangman = None


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    # sender_id = db.Column(db.Integer,
    #                       db.ForeignKey('user.u_id'),
    #                       nullable=False)
    channel_id = db.Column(db.Integer,
                           db.ForeignKey('channel.channel_id'),
                           nullable=False)
    message = db.Column(db.String(1000))
    time_created = db.Column(db.DateTime)
    reacts = db.relationship("React", backref="message", lazy=True)
    is_pinned = db.Column(db.Boolean)

    def __repr__(self):
        return f'{self.time_created}: {self.message}'


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
            'u_ids': self.users,
            'is_this_user_reacted': self in user.reacts
        }


class ExpiredToken(db.Model):
    token_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500))

    def __init__(self, token):
        self.token = token


db.create_all()