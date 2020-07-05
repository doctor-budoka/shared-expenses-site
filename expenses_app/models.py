import datetime as dt

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class AuthorisedEmail(db.Model):
    email_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    user = db.relationship("User", uselist=False, back_populates="email")
    is_registered = db.Column(db.Boolean, default=False)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey("authorised_email.email_id"), unique=True, index=True)
    email = db.relationship("AuthorisedEmail", back_populates="user")
    password_hash = db.Column(db.String(128))
    time_joined = db.Column(db.DateTime, default=dt.datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"