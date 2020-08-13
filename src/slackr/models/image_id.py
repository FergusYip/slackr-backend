from slackr import db


class ImageID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(15))
