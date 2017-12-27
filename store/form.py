from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, ValidationError, BooleanField, FloatField
from wtforms.validators import EqualTo, InputRequired, Email, Length, NumberRange
from model import User, Module, Goods
from hashlib import sha256
from utils import get_memcache_data


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

    def validate_username(self, field):
        username = field.data
        user = User.query.filter_by(username=username).first()
        if user:
            self.errors["user"] = "the username is exist"
            return False

    def validate_captcha(self, field):
        captcha = field.data
        rs = get_memcache_data(captcha)
        if not rs or rs != captcha.lower():
            self.errors["captcha"] = "the captcha is exist"
            return False


class Add_goods(FlaskForm):
    name = StringField(validators=[InputRequired()])
    price = FloatField(validators=[NumberRange(0, 1000000), InputRequired()])
    number = StringField()
    goods_module = StringField()

    def validate_name(self, field):
        name = field.data
        goods = Goods.query.filter_by(name=name).first()
        if goods:
            self.errors["goods"] = "the goods name is exist"
            return False

    def validate_number(self, field):
        number = field.data
        if number and len(number) != 13:
            self.errors["number"] = "the goods number length is error"
            return False

    def validate_goods_module(self, field):
        goods_module_name = field.data
        goods_module = Module.query.filter_by(name=goods_module_name).first()
        if not goods_module:
            self.errors["goods_module"] = "goods_module not exist"
            return False
