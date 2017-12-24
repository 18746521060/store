from blinker import Namespace
import os

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
def set_memcache_data(data, time=60*5):
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
    rs = mc.delete(data)
    return rs



from flask_mail import Mail, Message
import flask

app = flask.Flask(__name__)

MAIL_SERVER = 'smtp.qq.com',
MAIL_PROT = 25,
MAIL_USE_TLS = True,
MAIL_USE_SSL = False,
MAIL_USERNAME = "2584688424@qq.com",
MAIL_PASSWORD = "wangbaichao1",
MAIL_DEBUG = True

mail = Mail(app)
sender = "2584688424@qq.com"

def send_mail(email,recipient , data):
    if isinstance(recipient, list):
        msg = Message("This is a test", sender=email, recipients=recipient)
    else:
        msg = Message("This is a test", sender=email, recipients=[recipient])
    mail.send(msg)
    print("send email ok")

# data = "Hello this is the email content"
# send_mail(sender, "2596279105@qq.com", data)