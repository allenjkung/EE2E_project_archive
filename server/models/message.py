import datetime

from server import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(255))
    username_to = db.Column(db.String(255))
    username_from = db.Column(db.String(255))
    message = db.Column(db.LargeBinary)
    time_sent = db.Column(db.DateTime, default=datetime.datetime.utcnow())
