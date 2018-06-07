# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import tornado.web


class TestHandler(tornado.web.RequestHandler):
    """Test healthy for this web server"""

    def data_received(self, chunk):
        """Implement this method to handle streamed request data.
        Requires the `.stream_request_body` decorator.
        Implement for tornado.web.RequestHandler
        """
        pass

    def get(self):
        self.write("Hello, world")
