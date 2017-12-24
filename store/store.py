#!/usr/bin/env python3
import flask
from flask import Flask
from flask_wtf import CSRFProtect
from flask.views import MethodView
import config as con
from model import db, User
from form import User_login, User_registe
from utils import signal_login
import time
from hashlib import sha256
from my_decorate import user_required

app = Flask(__name__)
app.config.from_object(con)
CSRFProtect(app)
db.init_app(app)


@app.route("/")
def origination():
    return flask.redirect(flask.url_for("index"))


@app.route("/index/")
@user_required
def index():
    return flask.render_template("overview.html")

@app.route("/module_manager/")
@user_required
def module_manager():
    return flask.render_template("module.html")

@app.route("/add_goods/")
@user_required
def add_goods():
    return flask.render_template("add_goods.html")

@app.route("/goods_manager/")
@user_required
def goods_manager():
    return flask.render_template("goods_manage.html")


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
            return flask.jsonify(form.errors)


app.add_url_rule("/regist/", view_func=My_regist.as_view("regist"))


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
