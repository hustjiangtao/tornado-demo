# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Base handler for requests handlers"""


import json
import tornado.web
import functools

from tornado.web import HTTPError

from lib.system_code import FAIL
from lib.system_code import MESSAGE


def authenticated(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # if not self.current_user:
        #     raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


class BaseHandler(tornado.web.RequestHandler):
    """Base class for other request handlers - all other handlers should
    base on this one.
    """

    def data_received(self, chunk):
        """Implement this method to handle streamed request data.
        Requires the `.stream_request_body` decorator.
        Implement for tornado.web.RequestHandler
        """
        pass

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
        if message == '':
            message = MESSAGE.get(code, FAIL)
        result = {
            "code": code,
            "message": message,
            "data": data,
        }
        self.write(json.dumps(result, ensure_ascii=False))

    def check_xsrf_cookie(self):
        """Adapt for ajax requests, exclude get, head and options"""
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return
