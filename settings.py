# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""settings for web server"""


import os

from tornado.options import define, options
from tornado.log import enable_pretty_logging

# options settings
define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="debug mode", type=bool)
options.parse_command_line()

# log settings
enable_pretty_logging()

# seetings for path
ROOT = os.path.dirname(os.path.abspath(__file__))

__BASE_PACKAGE__ = "app"
STATIC_PATH = os.path.join(ROOT, __BASE_PACKAGE__, 'static')
TEMPLATE_PATH = os.path.join(ROOT, __BASE_PACKAGE__, 'templates')

SETTINGS = {
    "debug": options.debug,
    "autoreload": options.debug,
    "static_path": STATIC_PATH,
    "template_path": TEMPLATE_PATH,
    "cookie_secret": '8WJl4eQB0FcSnRG3FcBz0cD35',
    "xsrf_cookies": True,
    "login_url": '/auth',
}
