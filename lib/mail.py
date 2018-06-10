# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import re
import base64
import smtplib

from tornado import gen

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.utils import formataddr


@gen.coroutine
def send_msg_by_email(mail_to, msg, to_name=None, subject=None, attach_file=None):
    if not mail_to:
        raise gen.Return(False)

    # 发送邮箱
    sender = '****@gmail.com'
    mail_pass = '****'

    # 第三方
    mail_host = 'smtp.gamil.com'  # 邮箱服务器
    mail_user = sender  # 用户名
    mail_pass = mail_pass  # 密码
    if not mail_pass:
        mail_pass = input('密码：')  # 手动输入密码

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
        smtpObj = smtplib.SMTP()
        smtpObj.connect(host=mail_host, port=25)  # 连接第三方服务器
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

    raise gen.Return(result)
    # return result
