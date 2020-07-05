import datetime as dt

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AuthorisedEmail(db.Model):
    email_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    user = db.relationship("User", uselist=False, back_populates="email")
    is_registered = db.Column(db.Boolean, default=False)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email_id = db.Column(db.Integer, db.ForeignKey("authorised_email.email_id"))
    email = db.relationship("AuthorisedEmail", back_populates="user")
    password_hash = db.Column(db.String(128))
    time_joined = db.Column(db.DateTime, default=dt.datetime.utcnow)
