#!/usr/bin/env python3
import flask
from flask_wtf import CSRFProtect
from flask.views import MethodView
import config as con
from model import db, User, Module, Goods
from form import User_login, User_registe, Add_goods
from utils import signal_login, mail, send_mail, get_captcha, set_memcache_data, get_form_error_data, get_price
import time
from hashlib import sha256
from exts import app
from my_decorate import user_required
from task import send_captcha_email

app.config.from_object(con)
CSRFProtect(app)
db.init_app(app)
mail.init_app(app)


@app.route("/")
def origination():
    return flask.redirect(flask.url_for("index"))


@app.route("/index/")
@user_required
def index():
    goods_modules = Module.query.all()
    goods = Goods.query.all()
    con = {
        "goods_modules": goods_modules,
        "goods": goods
    }
    return flask.render_template("overview.html", **con)


@app.route("/module_manager/", methods=["GET", "POST"])
@user_required
def module_manager():
    if flask.request.method == "GET":
        goods_modules = Module.query.all()
        con = {
            "goods_modules": goods_modules
        }
        return flask.render_template("module.html", **con)
    elif flask.request.method == "POST":
        old_name = flask.request.form.get("old_name", None)
        new_name = flask.request.form.get("new_name", None)
        goods_module = Module.query.filter_by(name=old_name).first()
        if not goods_module:
            return flask.jsonify({"code": 400, "message": "没有旧模块,请检查!"})
        goods_module.name = new_name
        db.session.commit()
        return flask.jsonify({"code": 200, "message": "修改成功!"})


@app.route("/delete_module/", methods=["POST"])
def delete_module():
    name = flask.request.form.get("name", None)
    if name:
        goods_module = Module.query.filter_by(name=name).first()
        if goods_module:
            db.session.delete(goods_module)
            db.session.commit()
            return flask.jsonify({"code": 200, "message": "删除成功!"})
        else:
            return flask.jsonify({"code": 400, "message": "没有该模块!"})
    else:
        return flask.jsonify({"code": 404, "message": "参数错误!"})


@app.route("/add_goods/", methods=["GET", "POST"])
@user_required
def add_goods():
    if flask.request.method == "GET":
        goods_modules = Module.query.all()
        con = {
            "goods_modules": goods_modules
        }
        return flask.render_template("add_goods.html", **con)
    elif flask.request.method == "POST":
        form = Add_goods(flask.request.form)
        if form.validate():
            module_name = form.goods_module.data
            name = form.name.data
            price = form.price.data
            number = form.number.data
            goods_module = Module.query.filter_by(name=module_name).first()
            goods = Goods(name=name, price=price, number=(number or None))
            goods.module = goods_module
            db.session.add(goods)
            db.session.commit()
            return flask.jsonify({"code": 200, "message": "添加该商品成功!"})
        else:
            message = get_form_error_data(form)
            return flask.jsonify({"code": 400, "message": message})


@app.route("/add_module/", methods=["GET", "POST"])
@user_required
def add_module():
    if flask.request.method == "GET":
        return flask.render_template("add_module.html")
    elif flask.request.method == "POST":
        name = flask.request.form.get("name", None)
        if not name:
            return flask.jsonify({"code": 404, "message": "参数错误!"})
        goods_modules = Module.query.filter_by(name=name).first()
        if goods_modules:
            return flask.jsonify({"code": 400, "message": "该模块已存在"})
        else:
            goods_module = Module(name=name)
            db.session.add(goods_module)
            db.session.commit()
            return flask.jsonify({"code": 200, "message": "添加模块成功!"})


@app.route("/check_module_name/", methods=["POST"])
def check_module_name():
    name = flask.request.form.get("name", None)
    if not name:
        return flask.jsonify({"code": 404, "message": "参数错误!"})
    goods_modules = Module.query.filter_by(name=name).first()
    if goods_modules:
        return flask.jsonify({"code": 400, "message": "该模块已存在"})
    else:
        return flask.jsonify({"code": 200, "message": "模块名通过!"})


@app.route("/goods_manager/")
@user_required
def goods_manager():
    goods_modules = Module.query.all()
    con = {
        "goods_modules": goods_modules
    }
    return flask.render_template("goods_manage.html", **con)


class My_login(MethodView):
    def get(self):
        con = {"title": "登录"}
        return flask.render_template("login.html", **con)

    def post(self):
        form = User_login(flask.request.form)
        if form.validate():
            remember = form.remember.data
            username = form.username.data
            flask.session[con.SESSION_NAME] = username
            if remember:
                flask.session.permanent = True
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            data = "%s %s 登陆成功!" % (now, username)
            signal_login.send(app, data=data)
            return flask.redirect(flask.url_for("index"))
        else:
            return flask.jsonify(form.errors)


app.add_url_rule("/login/", view_func=My_login.as_view("login"))


class My_regist(MethodView):
    def get(self):
        con = {"title": "注册"}
        return flask.render_template("regist.html", **con)

    def post(self):
        form = User_registe(flask.request.form)
        if form.validate():
            username = form.username.data
            password = form.passwrod.data
            password = sha256(str(password).encode("utf-8")).hexdgest()
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            data = {
                "code": 200,
                "message": "恭喜，注册成功!"
            }
            return flask.jsonify(data)
        else:
            message = get_form_error_data(form)
            data = {
                "code": 400,
                "message": message
            }
            return flask.jsonify(data)


app.add_url_rule("/regist/", view_func=My_regist.as_view("regist"))


@app.route("/get_captcha/", methods=["POST"])
def get_captcha_code():
    email = flask.request.form.get("email", None)
    user = User.query.filter_by(email=email).first()
    if email and not user:
        captcha_code = get_captcha(6)
        subject = "库管验证码"
        data = "欢迎注册仓库管理系统，您的注册码为:%s, 请您把注册码填写到注册页面中，该注册码30分钟内有效!" % captcha_code
        # state, rs = send_mail("库管验证码", email, data=data)
        # if state:
        #     set_memcache_data(captcha_code, 60 * 30)
        #     return flask.jsonify({"code": 200, "message": "恭喜，验证码发送成功!"})
        # else:
        #     return flask.jsonify({"code": 400, "message": str(rs)})
        send_captcha_email.delay(subject, email, body=data)
        return flask.jsonify({"code": 200, "message": "恭喜，验证码发送成功!"})


@app.route("/detail/<number>/")
def detail(number):
    goods = Goods.query.filter_by(number=number).first()
    goods_modules = Module.query.all()
    con = {
        "goods": goods,
        "goods_modules": goods_modules
    }
    return flask.render_template("detail.html", **con)


@app.route("/detail_goods/", methods=["POST"])
def detail_goods():
    old_number = flask.request.form.get("old_number", None)
    name = flask.request.form.get("name", None)
    price = flask.request.form.get("price", None)
    number = flask.request.form.get("number", None)
    goods_module = flask.request.form.get("module", None)
    remarks = flask.request.form.get("remarks", None)
    price = get_price(price)
    new_module = Module.query.filter_by(name=goods_module).first()
    if old_number:
        goods = Goods.query.filter_by(number=old_number).first()
        if goods:
            goods.name = name
            goods.price = price
            goods.number = number
            goods.module = new_module
            goods.remarks = remarks
            db.session.commit()
            return flask.jsonify({"code": 200, "message": "修改成功!"})
        return flask.jsonify({"code": 400, "message": "没有这个编码的物品,请检查编码!"})
    return flask.jsonify({"code": 404, "message": "编码参数错误!"})


@app.route("/seach/", methods=["POST"])
def seach():
    keyword = flask.request.form.get("keyword", None)
    if not keyword:
        return flask.jsonify({"code": 404, "message": "参数错误!"})
    rs1 = "%{}%".format(keyword)
    goods = Goods.query.filter(
        db.or_(Goods.name.like(rs1), Goods.number.like(rs1))).first()
    return flask.jsonify({"code": 200, "number": goods.number} if goods else {"code": 400, "message": "没有该商品"})


@app.errorhandler(404)
def error_html(error):
    con = {
        "title": "404 错误",
        "content": "您似乎来到没有知识的荒野!"
    }
    print(error)
    return flask.render_template("error.html", **con), 404


@app.context_processor
def login_username():
    username = flask.session.get(con.SESSION_NAME, None)
    if username:
        return {"login_username": username}
    else:
        return {}


if __name__ == '__main__':
    app.run()
