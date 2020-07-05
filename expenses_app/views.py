from flask import current_app as app, render_template, redirect, url_for, make_response, flash
from expenses_app.forms import LogInForm, Register
from expenses_app.models import db, AuthorisedEmail, User


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        email = AuthorisedEmail.query.filter(AuthorisedEmail.email == email).first()
        if email and email.user and email.user.check_password(password):
            user = email.user
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
        auth_email = AuthorisedEmail.query.filter_by(email=email).first()
        if auth_email and auth_email.is_registered:
            flash("You are already registered! Try logging in instead!")
        elif auth_email:
            password = form.password.data
            if User.register_user(auth_email, password):
                db.session.commit()
                return redirect(url_for("index"))
            else:
                # TODO: Handle these errors more nicely
                return make_response("Something went wrong with registration!", 500)
        else:
            flash("Email is not an authorised email! This is a private service.")
    return render_template("register.html", form=form)
