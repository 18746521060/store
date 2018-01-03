from flask_sqlalchemy import SQLAlchemy
import flask


app = flask.Flask("store")
db = SQLAlchemy()
