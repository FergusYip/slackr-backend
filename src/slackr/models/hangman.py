from slackr import db


class Hangman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=False)
    word = db.Column(db.String(100))
    guesses = db.Column(db.String(23), default='')
    incorrect = db.Column(db.String(23), default='')
    stage = db.Column(db.Integer, default=0)
    prev_msg_id = db.Column(db.Integer)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.channel_id'))
