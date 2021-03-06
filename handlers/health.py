# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import tornado.web

from handlers.base_handler import BaseHandler


class HealthHandler(BaseHandler):
    """Test healthy for this web server"""

    def get(self):
        code = 200
        message = "success"
        data = {
            "result": True,
        }

        self.render_json(code=code, data=data, message=message)
        return
