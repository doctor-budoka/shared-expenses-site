from flask import url_for, flash, render_template, make_response
from flask import Blueprint
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import redirect

from expenses_app import db, login_manager
from expenses_app.forms import LogInForm, Register
from expenses_app.models import AuthorisedEmail, User


auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        email = AuthorisedEmail.query.filter(AuthorisedEmail.email == email).first()
        if email and email.user and email.user.check_password(password):
            user = email.user
            login_user(user)
            return redirect(url_for("index"))
        else:
            # TODO: Limit number of retries
            flash("Invalid email or password!")

    return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data

        username_exists = User.query.filter_by(username=username).first()
        auth_email = AuthorisedEmail.query.filter_by(email=email).first()
        if auth_email and auth_email.is_registered:
            flash("You are already registered! Try logging in instead!")
        elif auth_email and username_exists:
            flash("That username already exists! Try another")
        elif auth_email:
            password = form.password.data
            user = User.create_user(auth_email, password, username)
            db.session.commit()
            if user:
                login_user(user)
                return redirect(url_for("index"))
            else:
                # TODO: Handle these errors more nicely
                return make_response("Something went wrong with registration!", 500)
        else:
            flash("Email is not an authorised email! This is a private service.")
    return render_template("register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))
