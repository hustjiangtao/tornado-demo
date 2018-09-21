# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Auth handler"""

from app.handlers.base_handler import BaseHandler
from app.handlers.base_handler import authenticated
from app.database.user import user_db

from app.lib.utils import json_encode
from app.lib.system_code import SUCCESS
from app.lib.system_code import PARAMS_MISS
from app.lib.system_code import ACCOUNT_ERROR
from app.lib.system_code import PASSWORD_ERROR


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

    @authenticated
    def delete(self):
        """logout api"""
        self.clear_cookie('user')

        code = SUCCESS
        data = None

        self.render_json(code=code, data=data)

    def get(self):
        """login page"""
        next_url = self.get_query_argument('next', '')

        user_id = self.current_user
        if user_id:
            self.redirect('/user')
        else:
            data = {
                "next": next_url,
            }
            self.render('user/auth.html', data=data)
