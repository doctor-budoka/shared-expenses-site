from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, FloatField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo


class LogInForm(FlaskForm):
    email = StringField("Email", [
        InputRequired(message="You must provide an email address to continue"),
        Email(message="Email entered is not a valid email address")])
    password = PasswordField("Password", [InputRequired(message="You must provide a password to continue")])
    submit = SubmitField("Submit")


class Register(FlaskForm):
    email = StringField("Email", [
        InputRequired(message="You must provide an email address to continue"),
        Email(message="Email entered is not a valid email address")])
    username = StringField(
        "Username", [InputRequired(message="You must profice a username to continue")]
    )
    password = PasswordField("Password", [InputRequired(message="You must provide a password to continue")])
    confirm = PasswordField("Confirm", [
        InputRequired(message="You must provide a password to continue"),
        EqualTo("password", message="Password and confirmation must be the same!")
    ])
    submit = SubmitField("Submit")


class CreateGroup(FlaskForm):
    name = StringField("Name", [InputRequired(message="You must provide a name for the group!")])
    create = SubmitField("Create")


class AddUserToGroup(FlaskForm):
    username = StringField("Username", [InputRequired(message="You must provide a name for the user!")])
    add = SubmitField("Add")


class RemoveUserFromGroup(FlaskForm):
    username = SelectField(
        "Username", coerce=int, validators=[InputRequired(message="You must provide a user to remove!")])
    remove = SubmitField("Remove")


class AddAccountToGroup(FlaskForm):
    name = StringField("Name", [InputRequired(message="You must provide a name for the account!")])
    user = SelectField("User", coerce=int, default=-1)
    starting_balance = FloatField("Starting Balance")
    has_balance = BooleanField("Has Balance?", default=False)
    add = SubmitField("Add")


class RemoveAccountFromGroup(FlaskForm):
    name = SelectField(
        "Name", coerce=int, validators=[InputRequired(message="You must provide an account to be removed!")])
    remove = SubmitField("Remove")
