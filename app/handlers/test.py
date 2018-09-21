# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Test"""


from app.handlers.base_handler import BaseHandler


class TestHandler(BaseHandler):
    """Test healthy for this web server"""

    def get(self):
        self.write("Hello, world")
