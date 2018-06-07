# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado import gen

from handlers.base_handler import BaseHandler
from handlers.base_handler import authenticated

from lib.system_code import SUCCESS
from lib.system_code import PARAMS_ERROR

from database.service.user_service import get_user_by_name


class UserHandler(BaseHandler):
    """User handler"""

    @gen.coroutine
    def post(self):
        account = self.get_query_argument('account', None)

        code = SUCCESS
        data = None

        if not account:
            code = PARAMS_ERROR
        else:
            data = True

        self.render_json(code=code, data=data)
        return

    @authenticated
    @gen.coroutine
    def put(self):
        account = self.get_query_argument('account', None)

        code = SUCCESS
        data = None

        if not account:
            code = PARAMS_ERROR
        else:
            data = True

        self.render_json(code=code, data=data)
        return

    @authenticated
    @gen.coroutine
    def get(self):
        account = self.get_query_argument('account', None)

        code = SUCCESS
        data = None

        if not account:
            code = PARAMS_ERROR
        else:
            user = yield get_user_by_name(name=account)
            if user:
                data = {
                    "user_id": user.get('id'),
                    "user_account": user.get('account'),
                    "user_name": user.get('name'),
                    "user_email": user.get('email'),
                }

        self.render_json(code=code, data=data)
        return
