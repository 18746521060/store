from exts import db
import random
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json


def get_number():
    data = "0123456789101112003456789654987"
    return "".join(random.sample(data, 13))


auth_dict = {
    1: "普通用户权限",
    100: "高级用户权限"
}


class My_base(object):
    def to_dict(self):
        self_dict = {}
        if isinstance(self, db.Model):
            columns = self.__table__.columns
            for column in columns:
                value = getattr(self, column.name)
                if isinstance(column, datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                self_dict[column.name] = value
        else:
            self_dict = self.__dict__
        return self_dict

    def to_json(self, key=None, value=None):
        self_dict = self.to_dict()
        if key and value:
            self_dict[key] = value
        self_json = json.dumps(self_dict)
        return self_json


class User(My_base, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    auth = db.Column(db.Integer, default=1)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        # self._password = hashlib.sha256(pwd).hexdigest()
        self._password = generate_password_hash(pwd)

    def check_pwd(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return "User(id:%s,username:%s,password:%s,auth:%s)" % (
            self.id, self.username, self.password, auth_dict.get(self.auth))


class Module(My_base, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)

    goods = db.relationship("Goods", backref="module", passive_deletes=True, cascade="all, delete-orphan")

    def __repr__(self):
        return "Module(id:%s,name:%s)" % (self.id, self.name)


class Goods(My_base, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    number = db.Column(db.String(13), nullable=False, default=get_number)
    remarks = db.Column(db.Text)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id", ondelete="CASCADE"))

    def __repr__(self):
        return "Goods(id:%s,name:%s,price:%s,number:%s,remark:%s,module_id:%s)" % (
            self.id, self.name, self.price, self.number, self.remarks, self.module_id)
