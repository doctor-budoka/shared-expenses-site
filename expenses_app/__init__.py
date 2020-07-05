from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")

    with app.app_context():
        from expenses_app.views import index, login
    return app
