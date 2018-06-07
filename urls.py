# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""url handlers for web server"""


from handlers.test import TestHandler
from handlers.health import HealthHandler
from handlers.auth import AuthHandler
from handlers.user import UserHandler
from handlers.post import PostHandler


url_handlers = [
    (r"/test", TestHandler),
    (r"/health", HealthHandler),
    (r"/auth", AuthHandler),
    (r"/user", UserHandler),
    (r"/post", PostHandler),
]
