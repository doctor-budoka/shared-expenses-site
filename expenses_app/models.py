import datetime as dt

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class AuthorisedEmail(db.Model):
    email_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    user = db.relationship("User", uselist=False, back_populates="email")
    is_registered = db.Column(db.Boolean, nullable=False, default=False)

    def register_user(self, user):
        if self.is_registered:
            return False
        self.user = user
        self.is_registered = True
        return True


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(
        db.Integer,
        db.ForeignKey("authorised_email.email_id"),
        unique=True,
        index=True,
        nullable=False
    )
    email = db.relationship("AuthorisedEmail", back_populates="user")
    password_hash = db.Column(db.String(128), nullable=False)
    time_joined = db.Column(db.DateTime, default=dt.datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create_user(cls, email, password):
        new_user = cls()
        new_user.set_password(password)
        new_user.email = email
        if email.register_user(new_user):
            return new_user
        else:
            return None

    def __repr__(self):
        return f"<User {self.username}>"
