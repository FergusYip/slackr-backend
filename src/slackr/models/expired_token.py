from slackr import db


class ExpiredToken(db.Model):
    token_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500))

    def __init__(self, token):
        self.token = token
