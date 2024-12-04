import datetime

from server import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    registration_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow())
