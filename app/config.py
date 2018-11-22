# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""config file"""


import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../', '.env'))

# sql
SQL = {
    "mysql": os.environ.get('SQLALCHEMY_DATABASE_URI_MYSQL'),
}

# mail
MAIL = {
    "server": os.environ.get('MAIL_SERVER'),
    "port": os.environ.get('MAIL_PORT'),
    "tls": os.environ.get('MAIL_USE_TLS'),
    "ssl": os.environ.get('MAIL_USE_SSL'),
    "username": os.environ.get('MAIL_USERNAME'),
    "password": os.environ.get('MAIL_PASSWORD'),
}

# weibo
WEIBO = {
    "account": os.environ.get('WEIBO_ACCOUNT'),
    "pass": os.environ.get('WEIBO_PASS'),
    "uid": int(os.environ.get('WEIBO_UID')),
}


__all__ = (
    SQL,
    MAIL,
    WEIBO,
)
