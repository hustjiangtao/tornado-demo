# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""url handlers for web server"""


from handlers.test import TestHandler
from handlers.health import HealthHandler
from handlers.user import UserHandler


url_handlers = [
    (r"/test", TestHandler),
    (r"/health", HealthHandler),
    (r"/user", UserHandler),
]
