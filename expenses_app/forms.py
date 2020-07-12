from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
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
