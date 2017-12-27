from blinker import Namespace
import os


def get_form_error_data(form):
    """get form error message from first"""
    return list(form.errors.values())[0]


dir_path = os.path.dirname(__file__)
file_path = os.path.join(dir_path, "store.log")
error_path = os.path.join(dir_path, "error.log")

namespace = Namespace()

signal_login = namespace.signal("login")


def login_log(render, data):
    data += "\n"
    try:
        with open(file_path, "a+", encoding="utf-8") as f:
            f.write(data)
        print("登录日志保存成功!")
    except Exception as e:
        with open(error_path, "a+", encoding="utf-8") as f:
            f.write(e)
        print("登陆日志保存失败!请查看错误log文件!")


signal_login.connect(login_log)

import string
import random


def get_captcha(count):
    """captcha func"""
    data = string.ascii_letters + "0123456789"
    rs = random.sample(data, count)
    return "".join(rs)


# print(get_captcha(6))


import memcache

mc = memcache.Client(["127.0.0.1:11211"], debug=True)


def set_memcache_data(data, time=60 * 5):
    """set memcache data"""
    data = data.lower()
    mc.set(data, data, time=time)
    return True


def get_memcache_data(data):
    """get memcache data"""
    data = data.lower()
    rs = mc.get(data)
    return rs


def delete_memcache_data(data):
    """delete mecache data"""
    data = data.lower()
    rs = mc.delete(data)
    return rs


from flask_mail import Mail, Message
# import flask
#
# app = flask.Flask(__name__)
# app.config.update(
#     MAIL_SERVER='smtp.qq.com',
#     MAIL_PORT=465,
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME='2584688424@qq.com',
#     MAIL_PASSWORD='heegkqckptljecde',
#     MAIL_DEFAULT_SENDER='2584688424@qq.com'
# )

# mail = Mail(app)
mail = Mail()


def send_mail(subject, recipient, data=None, html=None):
    """send the email captcha"""
    assert recipient
    if isinstance(recipient, list):
        msg = Message(subject, recipients=recipient, body=data, html=html)
    else:
        msg = Message(subject, recipients=[recipient], body=data, html=html)
    try:
        mail.send(msg)
        return True, "ok"
    except Exception as e:
        print("e:", e)
        return False, e



