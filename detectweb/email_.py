from threading import Thread

from flask import current_app
from flask_mail import Message
from detectweb import mail

# 异步发送邮件函数
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body):
    # subject主题，接收者，
    msg = Message(
        subject=subject,
        recipients=recipients,
        reply_to='noreply@detectweb.com' # 不写sender而写reply_to，使得收到的邮件都被这个邮箱自动删除
    )
    # 文本body
    msg.body = text_body
    # 看收到邮件的客户端，如果不支持html格式显示，那就用text显示
    msg.html = html_body
    # 多线程发送，为了点击发送邮件后不卡住，大概会卡住3-4秒等待邮件去发
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)).start()
