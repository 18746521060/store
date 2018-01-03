from celery import Celery, Task
from utils import send_mail
from exts import app


# borker url 格式：redis://:password@hostname:port/db_number

def make_celery(app):
    my_celery = Celery(app.import_name, backend="redis://:192.168.237.132:6379/0",
                       broker="redis://:192.168.237.132:6379/0")

    class ContextTask(Task):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return Task.__call__(self, *args, **kwargs)
    my_celery.Task = ContextTask
    return my_celery

celery = make_celery(app)

@celery.task
def send_captcha_email(subject, recipient, body=None, html=None):
    with app.app_content():
        send_mail(subject, recipient, body, html)
