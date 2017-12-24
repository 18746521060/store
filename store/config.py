import os


DEBUG = True
SECRET_KEY = os.urandom(24)
DB_URI = "sqlite:///store.sql"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

SESSION_NAME = "youGuess"