import click
from flask import current_app as app
from expenses_app.models import db, AuthorisedEmail, User


@app.cli.command("reset-db")
def reset_db():
    """Used to reset the db for the app"""
    click.echo("Resetting db...")
    db.drop_all()
    db.create_all()
    click.echo("Done")


@app.cli.command("create-auth-emails")
@click.argument("emails", nargs=-1)
def create_authorised_emails(emails):
    """Adds emails to the Authorised emails db"""
    click.echo("Emails added to authorised_email:")
    if emails:
        for email in emails:
            click.echo(f"\t'{email}'")
            new_email = AuthorisedEmail()
            new_email.email = email
            db.session.add(new_email)
        db.session.commit()


@app.cli.command("create-user")
@click.argument("username")
@click.argument("password")
@click.argument("email")
def create_user(username, password, email):
    """Adds a user to the db"""
    click.echo(f"Creating user with email='{email}', username='{username}'")
    auth_email = AuthorisedEmail.query.filter_by(email=email).first()
    if auth_email:
        User.create_user(auth_email, password, username)
        db.session.commit()
    else:
        raise ValueError(f"{email} is not an authorised email address!")
