from flask import Flask
from expenses_app.models import db
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from expenses_app.auth import auth
        app.register_blueprint(auth.auth_bp)

        from expenses_app.group import group
        app.register_blueprint(group.grp_bp)

        from expenses_app import commands

        db.create_all()
    return app
