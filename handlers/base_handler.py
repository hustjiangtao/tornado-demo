# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Base handler for requests handlers"""


import json
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """Base class for other request handlers - all other handlers should
    base on this one.
    """

    def initialize(self):
        self.__set_header()

    def __set_header(self):
        self.set_header("Server", "DemoServer")
        self.set_header("Cache-Control", "private")
        self.set_header('Version', 'v0.1')
        self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.set_header('Access-Control-Allow-Methods', 'POST, PUT, GET, OPTIONS, DELETE')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header(
            'Access-Control-Allow-Headers',
            'Origin, X-Requested-With, Content-Type, Accept, client_id, uuid, Authorization'
        )

        # # TODO test-only
        # self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin') or '*')

    def render_json(self, code=0, data=None, message=''):
        result = {
            "code": code,
            "message": message,
            "data": data,
        }
        self.write(json.dumps(result, ensure_ascii=False))
