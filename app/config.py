# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""config file"""


import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../', '.env'))

# weibo
WEIBO = {
    "account": os.environ.get('WEIBO_ACCOUNT'),
    "pass": os.environ.get('WEIBO_PASS'),
    "uid": int(os.environ.get('WEIBO_UID')),
}


__all__ = (
    WEIBO,
)
