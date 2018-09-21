# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Register"""


from app.handlers.base_handler import BaseHandler
from app.database.user import user_db

from app.lib.utils import json_encode
from app.lib.system_code import SUCCESS
from app.lib.system_code import PARAMS_MISS
from app.lib.system_code import ACCOUNT_USED


class RegisterHandler(BaseHandler):
    """Register handler"""

    def post(self):
        """Register api"""
        name = self.get_json_argument('name', None)
        email = self.get_json_argument('email', None)
        mobile = self.get_json_argument('mobile', None)
        password = self.get_json_argument('password', None)
        password_confirm = self.get_json_argument('password_confirm', None)

        code = SUCCESS
        data = None

        if not all([name, email, mobile, password, password_confirm]):
            code = PARAMS_MISS
        elif password != password_confirm:
            code = PARAMS_MISS
        else:
            user = user_db.get_user_auth_by_name(name=name)
            if user:
                code = ACCOUNT_USED
            else:
                my_password, my_salt = self.get_new_password(password)
                add_item = {
                    "name": name,
                    "email": email,
                    "mobile": mobile,
                    "password": my_password,
                    "salt": my_salt,
                }
                user_id = user_db.add_user(add_item)
                if user_id:
                    self.set_secure_cookie("user", json_encode(user_id))
                    data = {
                        "id": user_id,
                    }

        self.render_json(code=code, data=data)
