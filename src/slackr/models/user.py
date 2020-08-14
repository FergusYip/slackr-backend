from slackr import db, helpers
from slackr.utils.constants import PERMISSIONS
from slackr.models import user_react_identifier


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
    standups = db.relationship('Standup', backref='starting_user')

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
            'profile_img_url': self.profile_img_url
        }
