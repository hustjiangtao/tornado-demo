# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""url handlers for web server"""


from handlers.test import TestHandler
from handlers.health import HealthHandler


url_handlers = [
    (r"/test", TestHandler),
    (r"/health", HealthHandler),
]
