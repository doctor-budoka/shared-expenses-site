from flask import Flask
from expenses_app.models import db


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")
    db.init_app(app)

    with app.app_context():
        from expenses_app import views
        if app.config["RESET_DB"]:
            db.drop_all()

        db.create_all()
    return app
