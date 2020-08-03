from os import environ
from pathlib import Path
from dotenv import load_dotenv

BASE_DIRECTORY = Path(__file__).parent
load_dotenv(BASE_DIRECTORY / ".env")


class Config:
    FLASK_ENV = "development"
    TESTING = True
    DEBUG = True
    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Database values
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
