# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Mail service"""


import re
import base64
import smtplib
import logging
import traceback

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.utils import formataddr

from tornado import gen

from app.config import MAIL


logging.basicConfig(level=logging.INFO)


def send_msg_by_email(mail_to, msg, to_name=None, subject=None, attach_file=None):
    """send mail sync"""
    if not mail_to:
        return False

    # 第三方服务器配置
    mail_host = MAIL.get('server')  # 邮箱服务器
    mail_port = MAIL.get('port')  # 邮箱服务器
    mail_user = MAIL.get('username')  # 用户名
    mail_pass = MAIL.get('password')  # 密码
    if not mail_pass:
        mail_pass = input('密码：')  # 手动输入密码
    # 发送邮箱
    sender = mail_user

    if not msg:
        msg = '你好'  # 消息内容

    # message = MIMEText(msg, 'plain', 'utf-8')  # 纯文本
    message = MIMEMultipart()  # html
    message['From'] = formataddr(['注册', sender])
    message['To'] = formataddr([to_name, mail_to])
    message['Subject'] = subject or '注册服务'
    message.attach(MIMEText(msg, 'html', 'utf-8'))

    # 附件处理
    if attach_file:
        for x in attach_file:
            filename = x['filename']
            file = x['body']
            # filetype = x['content_type'].split('/')[-1]
            attach = MIMEApplication(file)
            attach.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(attach)

    try:
        # smtpObj = smtplib.SMTP('localhost')  # 本地发送
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(host=mail_host, port=mail_port)  # 连接第三方服务器
        smtpObj.login(user=mail_user, password=mail_pass)
        try:
            smtpObj.sendmail(sender, mail_to, message.as_string())
        except:
            msgImages = re.findall(r'src="(.+)" style', msg)
            for x in msgImages:
                msg = re.subn(r'data:image(.+)100%;', 'cid:'+str(msgImages.index(x)), msg)
                img = MIMEImage(base64.b64decode(x.split(',')[-1]))
                message.attach(img)
                smtpObj.sendmail(sender, mail_to, message.as_string())
        smtpObj.quit()
        result = True
    except smtplib.SMTPException:
        result = False
        logging.info(traceback.format_exc())

    return result


@gen.coroutine
def send_msg_by_email_async(mail_to, msg, to_name=None, subject=None, attach_file=None):
    """send mail async"""
    result = send_msg_by_email(mail_to, msg, to_name, subject, attach_file)
    raise gen.Return(result)
