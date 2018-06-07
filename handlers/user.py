# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from handlers.base_handler import BaseHandler
from database.user import user_db

from lib.utils import json_encode
from lib.system_code import SUCCESS
from lib.system_code import PARAMS_MISS
from lib.system_code import ACCOUNT_ERROR
from lib.system_code import PASSWORD_ERROR


class UserHandler(BaseHandler):
    """User handler"""

    def post(self):
        account = self.get_json_argument('account', None)
        password = self.get_json_argument('password', None)

        code = SUCCESS
        data = None

        if not all([account, password]):
            code = PARAMS_MISS
        else:
            user = user_db.get_user_by_name(name=account)
            if not user:
                code = ACCOUNT_ERROR
            else:
                self.set_secure_cookie("user", json_encode(user.get('id')))
                data = {
                    "result": True
                }

        self.render_json(code=code, data=data)
        return

    def get(self):

        self.render('user/auth.html')
