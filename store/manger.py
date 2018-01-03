from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from exts import db
from store import app
import model
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import sha256


manger = Manager(app)
migrate = Migrate(app, db)
manger.add_command("db", MigrateCommand)


@manger.option("-u", dest="username")
@manger.option("-p", dest="password")
@manger.option("-a", dest="auth")
def registe(username, password, auth=1):
    """用户注册"""
    # password = sha256(str(password).encode("utf-8")).hexdigest()
    user = model.User(username=username, password=password, auth=auth)
    db.session.add(user)
    db.session.commit()
    print("用户:%s,添加完成" % username)


@manger.option("-u", dest="username")
def delete_user(username):
    """删除用户"""
    user = model.User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print("删除%s用户成功" % username)
    else:
        print("没有该用户")


@manger.option("-u", dest="username")
def select_user(username):
    """查询用户信息"""
    user = model.User.query.filter_by(username=username).first()
    print(user if user else "没有该用户名")


@manger.option("-u", dest="username")
@manger.option("-p", dest="password")
def update_user(username, password):
    """修改用户密码"""
    user = model.User.query.filter_by(username=username).first()
    if not user:
        return "没有%s用户!" % username
    user.password = sha256(str(password).encode("utf-8")).hexdigest()
    db.session.commit()
    print("修改%s密码成功!" % username)


# @manger.command
# def add_number():
#     goods = model.Goods.query.filter_by(name="康师傅方便面(袋)").first()
#     goods.number = model.get_number()
#     db.session.commit()
#     print("添加 number success")

@manger.command
def check_goods():
    goods = model.Goods.query.all()
    print(goods)


@manger.command
def delete_goods():
    goods= model.Goods.query.first()
    db.session.delete(goods)
    db.session.commit()
    print("delete ok")


if __name__ == "__main__":
    manger.run()
