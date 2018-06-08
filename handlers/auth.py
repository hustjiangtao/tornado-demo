# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from handlers.base_handler import BaseHandler
from handlers.base_handler import authenticated
from database.user import user_db

from lib.utils import json_encode
from lib.system_code import SUCCESS
from lib.system_code import PARAMS_MISS
from lib.system_code import ACCOUNT_ERROR
from lib.system_code import PASSWORD_ERROR


class AuthHandler(BaseHandler):
    """Auth handler"""

    def post(self):
        """login api"""
        account = self.get_json_argument('account', None)
        password = self.get_json_argument('password', None)

        code = SUCCESS
        data = None

        if not all([account, password]):
            code = PARAMS_MISS
        else:
            user = user_db.get_user_auth_by_name(name=account)
            if not user:
                code = ACCOUNT_ERROR
            else:
                user_password = user.get('password')
                user_salt = user.get('salt')
                check_user_password = self.is_my_password(password, user_password, user_salt)
                if not check_user_password:
                    code = PASSWORD_ERROR
                else:
                    self.set_secure_cookie("user", json_encode(user.get('id')))
                    data = {
                        "result": True,
                        "next": ''
                    }

        self.render_json(code=code, data=data)
        return

    @authenticated
    def delete(self):
        """logout api"""
        self.clear_cookie('user')

        code = SUCCESS
        data = None

        self.render_json(code=code, data=data)
        return

    def get(self):
        """login page"""
        next = self.get_query_argument('next', '')

        user_id = self.get_secure_cookie('user')
        if user_id:
            self.redirect('/user')
        else:
            data = {
                "next": next,
            }
            self.render('user/auth.html', data=data)
