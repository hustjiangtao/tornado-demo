# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from handlers.base_handler import BaseHandler
from handlers.base_handler import authenticated
from database.user import user_db

from lib.utils import json_encode
from lib.system_code import SUCCESS
from lib.system_code import PARAMS_MISS
from lib.system_code import ACCOUNT_ERROR
from lib.system_code import USER_NOT_LOGIN
from lib.system_code import UPDATE_FAILED


class UserHandler(BaseHandler):
    """User handler"""

    @authenticated
    def put(self):
        """user update api"""
        name = self.get_json_argument('name', None)
        email = self.get_json_argument('email', None)
        mobile = self.get_json_argument('mobile', None)

        code = SUCCESS
        data = None

        user_id = self.get_secure_cookie('user')

        if not user_id:
            code = USER_NOT_LOGIN
        elif not all([name, email, mobile]):
            code = PARAMS_MISS
        else:
            user = user_db.get_user_by_id(id=user_id)
            if not user:
                code = ACCOUNT_ERROR
            else:
                update_item = {
                    "id": int(user_id),
                    "name": name,
                    "email": email,
                    "mobile": mobile,
                }
                result = user_db.update_user(item=update_item)
                if not result:
                    code = UPDATE_FAILED

        self.render_json(code=code, data=data)
        return

    @authenticated
    def get(self):
        """user info page"""
        user_id = self.get_secure_cookie('user')
        user = user_db.get_user_by_id(id=user_id)
        self.clear_cookie('user')
        if user:
            user = {
                "name": user.get('name') or '',
                "email": user.get('email') or '',
                "mobile": user.get('mobile') or '',
                "create_time": user.get('create_time'),
            }
        else:
            user = {}
        data = {
            "user": user,
        }
        self.render('user/user_info.html', data=data)
