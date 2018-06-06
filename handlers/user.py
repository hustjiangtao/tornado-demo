# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from handlers.base_handler import BaseHandler
from database.user import user_db


class UserHandler(BaseHandler):
    """User handler"""

    def post(self):
        account = self.get_json_argument('account', None)
        password = self.get_json_argument('password', None)
        print(account, password)

    def get(self):
        code = 200
        message = "success"
        data = {
            "result": True,
        }

        self.render('user/auth.html')
        # self.render('base.html')
        # self.render('auth.html')
