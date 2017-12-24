from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, ValidationError, BooleanField
from wtforms.validators import EqualTo, InputRequired, Email, Length
from model import User
from hashlib import sha256


class User_login(FlaskForm):
    username = StringField(validators=[Email()])
    password = StringField(validators=[Length(min=3)])
    remember = BooleanField()

    def validate(self):
        rs = super(User_login, self).validate()
        if not rs:
            return rs
        username = self.username.data
        password = self.password.data
        password = sha256(str(password).encode("utf-8")).hexdigest()
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return True
        else:
            self.errors["error"] = "username or password is error"
            return False


class User_registe(FlaskForm):
    username = StringField(validators=[Email()])
    password = StringField(validators=[Length(min=3)])
    password_repeat = StringField(validators=[EqualTo("password")])
    captcha = StringField(validators=[Length(min=6, max=6)])

    def validate_username(self):
        username = self.username.data
        user = User.query.filter_by(username=username).first()
        if user:
            self.errors["user"] = "the username is exist"
            return False