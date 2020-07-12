from flask import current_app as app, render_template, redirect, url_for, make_response, flash
from flask_login import login_user, login_required, logout_user, current_user
from expenses_app.forms import LogInForm, Register, CreateGroup
from expenses_app.models import db, AuthorisedEmail, User, Group
from expenses_app import login_manager


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = CreateGroup()
    if form.validate_on_submit():
        new_group_name = form.name.data
        exists = Group.query.filter(Group.name == new_group_name).first()
        if not exists:
            current_user.create_group(new_group_name)
            db.session.commit()
        else:
            flash(f"{new_group_name} has already been taken! Try another name.")
    return render_template("index.html", form=form)


@app.route("/groups/<group_name>/summary", methods=["GET", "POST"])
@login_required
def group_summary(group_name):
    group = group_from_group_name(group_name)

    if group and group.has_user(current_user):
        return render_template("group_summary.html", group=group)

    return redirect(url_for("index"))


@app.route("/groups/<group_name>/access", methods=["GET", "POST"])
@login_required
def group_access(group_name):
    group = group_from_group_name(group_name)
    if group and group.has_user(current_user):
        return render_template("group_access.html", group=group)

    return render_template("index.html", group=group)


def group_from_group_name(group_name):
    return Group.query.filter(Group.name == group_name).first()


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        email = AuthorisedEmail.query.filter(AuthorisedEmail.email == email).first()
        if email and email.user and email.user.check_password(password):
            user = email.user
            login_user(user)
            # TODO: log the user in
            return redirect(url_for("index"))
        else:
            # TODO: Limit number of retries
            flash("Invalid email or password!")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))
