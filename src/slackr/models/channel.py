from slackr import db
from slackr.models import owner_channel_identifier, user_channel_identifier
from slackr.models.standup import Standup


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
    standup = db.relationship('Standup', backref='channel', uselist=False)

    # hangman = None

    def __init__(self, user, name, is_public):
        self.name = name
        self.is_public = is_public
        self.all_members.append(user)
        self.owner_members.append(user)
        self.standup = Standup()

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
