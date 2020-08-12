from slackr import db


class User(db.Model):
    u_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name_first = db.Column(db.String(50), nullable=False)
    name_last = db.Column(db.String(50, nullable=False))
    handle_str = db.Column(db.String(20, nullable=False))
    permission_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.email}: {self.name_first}'