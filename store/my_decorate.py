from config import SESSION_NAME
import flask
from functools import wraps
from model import User


def user_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        username = flask.session.get(SESSION_NAME, None)
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                return func(*args, **kwargs)
        return flask.redirect(flask.url_for("login"))
    return wapper