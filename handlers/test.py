# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import tornado.web


class TestHandler(tornado.web.RequestHandler):
    """Test healthy for this web server"""

    def get(self):
        self.write("Hello, world")
