# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado import gen

from handlers.base_handler import BaseHandler
from handlers.base_handler import authenticated

from lib.system_code import SUCCESS
from lib.system_code import PARAMS_ERROR

from database.models.user import User


class AuthHandler(BaseHandler):
    """User handler"""

    @gen.coroutine
    def post(self):
        account = self.get_body_argument('account', None)
        password = self.get_body_argument('password', None)

        code = SUCCESS
        data = None

        if not all([account, password]):
            code = PARAMS_ERROR
        else:
            data = True

        self.render_json(code=code, data=data)
        return

    @authenticated
    @gen.coroutine
    def delete(self):
        account = self.get_body_argument('account', None)

        code = SUCCESS
        data = None

        if not account:
            code = PARAMS_ERROR
        else:
            data = True

        self.render_json(code=code, data=data)
        return
