# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""User"""


from app.handlers.base_handler import BaseHandler
from app.handlers.base_handler import authenticated
from app.database.user import user_db

from app.lib.system_code import SUCCESS
from app.lib.system_code import PARAMS_MISS
from app.lib.system_code import USER_NOT_LOGIN
from app.lib.system_code import UPDATE_FAILED


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

        user_id = self.current_user

        if not user_id:
            code = USER_NOT_LOGIN
        elif not all([name, email, mobile]):
            code = PARAMS_MISS
        else:
            update_item = {
                "name": name,
                "email": email,
                "mobile": mobile,
            }
            result = user_db.update_user(_id=user_id, item=update_item)
            if not result:
                code = UPDATE_FAILED

        self.render_json(code=code, data=data)

    @authenticated
    def get(self):
        """user info page"""
        user_id = self.current_user
        user = user_db.get_user_by_id(_id=user_id)
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
