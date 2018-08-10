# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""settings for web server"""


import os

from tornado.options import define, options
from tornado.log import enable_pretty_logging

# options settings
define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="debug mode", type=bool)
options.parse_command_line()

# log settings
enable_pretty_logging()

# seetings for path
ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT, 'static')
# TEMPLATE_PATH = os.path.join(ROOT, 'templates')
TEMPLATE_PATH = os.path.join(ROOT, 'tmp-mdl')

SETTINGS = {
    "debug": options.debug,
    "autoreload": False,
    "static_path": STATIC_PATH,
    "template_path": TEMPLATE_PATH,
    "cookie_secret": 'tornado-demo',
    "xsrf_cookies": True,
    "login_url": '/auth',
}
