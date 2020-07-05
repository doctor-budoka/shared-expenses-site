from flask import current_app as app, render_template, redirect, url_for
from expenses_app.forms import LogInForm


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("login.html", form=form)
