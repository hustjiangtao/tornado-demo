# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""url handlers for web server"""


from tornado.web import RedirectHandler

from handlers.test import TestHandler
from handlers.health import HealthHandler
from handlers.demo import DemoHandler
from handlers.register import RegisterHandler
from handlers.auth import AuthHandler
from handlers.user import UserHandler
from handlers.post_list import PostListHandler
from handlers.post import PostHandler
from handlers.chat import ChatIndexHandler
from handlers.chat import ChatHandler


url_handlers = [
    (r"/", RedirectHandler, dict(url='/posts', permanent=False)),
    (r"/test", TestHandler),
    (r"/health", HealthHandler),
    (r"/demo", DemoHandler),
    (r"/register", RegisterHandler),
    (r"/auth", AuthHandler),
    (r"/user", UserHandler),
    (r"/posts", PostListHandler),
    (r"/post", PostHandler),
    (r"/chat-index", ChatIndexHandler),
    (r"/chat", ChatHandler),
]
