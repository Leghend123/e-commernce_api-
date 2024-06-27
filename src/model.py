from datetime import datetime
from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    profile = db.Column(db.String(120), unique=False,
                        nullable=False, default='profile.jpg')
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self) -> str:
        return "User>>>{self.username}"
