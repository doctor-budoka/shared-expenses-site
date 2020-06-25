from flask import current_app


@current_app.route("/")
def index():
    return "Hello!"
