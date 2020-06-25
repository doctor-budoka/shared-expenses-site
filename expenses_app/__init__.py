from flask import Flask
from os.path import abspath


def create_app():
    app = Flask(__name__, template_folder="templates")
    with app.app_context():
        from expenses_app.views import index
    return app
