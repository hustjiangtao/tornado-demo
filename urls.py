# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""url handlers for web server"""


from handlers.test import TestHandler
from handlers.health import HealthHandler
from handlers.user import UserHandler
from handlers.post_list import PostListHandler
from handlers.post import PostHandler


url_handlers = [
    (r"/test", TestHandler),
    (r"/health", HealthHandler),
    (r"/user", UserHandler),
    (r"/posts", PostListHandler),
    (r"/post", PostHandler),
]
