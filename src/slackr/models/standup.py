from slackr import db


class Standup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=False)
    starting_u_id = db.Column(db.Integer, db.ForeignKey('user.u_id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.channel_id'))
    time_finish = db.Column(db.Integer)
    message = db.Column(db.String(1000), default='')
