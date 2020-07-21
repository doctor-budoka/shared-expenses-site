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

    def __repr__(self):
        return f"<AuthEmail {self.email}>"


group_membership_table = db.Table(
    "group_membership", db.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"))
)


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
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    time_joined = db.Column(db.DateTime, default=dt.datetime.utcnow)
    owned_groups = db.relationship("Group", back_populates="owner")
    groups = db.relationship("Group", secondary=group_membership_table, back_populates="members")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create_user(cls, email, password, username):
        new_user = cls()
        new_user.set_password(password)
        new_user.email = email
        new_user.username = username
        if email.register_user(new_user):
            return new_user
        else:
            return None

    def create_group(self, name):
        new_group = Group()
        new_group.name = name
        new_group.owner = self
        new_group.members.append(self)
        self.groups.append(new_group)

    def __repr__(self):
        return f"<User {self.username}>"


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    owner = db.relationship("User", back_populates="owned_groups")

    members = db.relationship("User", secondary=group_membership_table, back_populates="groups")
    accounts = db.relationship("Account", back_populates="group")

    def has_user(self, user):
        return user in self.members

    def add_user(self, new_user):
        self.members.append(new_user)

    def remove_user(self, old_user):
        self.members.remove(old_user)

    def __repr__(self):
        return f"<Group {self.id}, {self.name}>"


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), index=True, nullable=False)
    group = db.relationship("Group", uselist=False, back_populates="accounts")
    is_avatar = db.Column(db.Boolean, nullable=False, default=False)
    avatar_for_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    avatar_for = db.relationship("User", uselist=False)
    has_balance = db.Column(db.Boolean, default=False, nullable=False)
    starting_balance = db.Column(db.Numeric, nullable=True)
    status = db.Column(db.Enum("live", "removed", name="account_status"), nullable=False, default="live")

    db.UniqueConstraint("name", "group_id", name="uix_group_name")


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)
    paid_by_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    on_behalf_of_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    description = db.Column(db.Text(200), nullable=True)
    store = db.Column(db.Text(100), nullable=True)
    amount = db.Column(db.Float, nullable=False)
