# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""url handlers for web server"""


from handlers.test import TestHandler
from handlers.health import HealthHandler
from handlers.register import RegisterHandler
from handlers.auth import AuthHandler
from handlers.user import UserHandler
from handlers.post_list import PostListHandler
from handlers.post import PostHandler


url_handlers = [
    (r"/test", TestHandler),
    (r"/health", HealthHandler),
    (r"/register", RegisterHandler),
    (r"/auth", AuthHandler),
    (r"/user", UserHandler),
    (r"/posts", PostListHandler),
    (r"/post", PostHandler),
]
