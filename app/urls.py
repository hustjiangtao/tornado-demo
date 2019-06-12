# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""url handlers for web server"""


from tornado.web import RedirectHandler
from tornado.web import url

from app.handlers.test import TestHandler
from app.handlers.health import HealthHandler
from app.handlers.demo import demo
from app.handlers.auth import register
from app.handlers.auth import auth
from app.handlers.user import user


URL_HANDLERS = []


__BASE_URL_HANDLERS = [
    url(r"/", RedirectHandler, dict(url='/health', permanent=False)),
    url(r"/test", TestHandler),
    url(r"/health", HealthHandler),
    url(r"/demo", demo.DemoHandler),
    url(r"/register", register.RegisterHandler),
    url(r"/auth", auth.AuthHandler),
    url(r"/user", user.UserHandler),
]


URL_HANDLERS.extend(__BASE_URL_HANDLERS)
