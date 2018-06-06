# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Base handler for requests handlers"""


import json
import tornado.web

from lib.utils import json_decode
from tornado.escape import to_unicode
from tornado.web import MissingArgumentError


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
        # self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.set_header('Content-Type', 'text/html; charset="utf-8"')
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

    def check_xsrf_cookie(self):
        """Ignore xsrf if ajax"""
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return

    def get_json_argument(self, name, default=None):
        """Get argument from application/json body"""
        content_type = self.request.headers.get("Content-Type", "")
        if content_type.startswith("application/json"):
            args = json_decode(self.request.body)
            name = to_unicode(name)
            if name in args:
                return args[name]
            elif default is not None:
                return default
            else:
                raise MissingArgumentError(name)
