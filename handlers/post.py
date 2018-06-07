# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from handlers.base_handler import BaseHandler
from database.post import post_db
from database.user import user_db
from lib.system_code import SUCCESS
from lib.system_code import PARAMS_MISS
from lib.system_code import POST_ADD_ERROR
from tornado.web import HTTPError


class PostHandler(BaseHandler):
    """Post handler"""

    def post(self):
        title = self.get_json_argument('title', None)
        content = self.get_json_argument('content', None)
        print(111)

        code = SUCCESS
        data = None

        if not all([title, content]):
            code = PARAMS_MISS
        else:
            current_user = user_db.get_user_by_id(id=self.current_user)
            add_item = {
                "title": title,
                "content": content,
                "author": current_user.get('name'),
            }
            result = post_db.add_post(item=add_item)
            if not result:
                code = POST_ADD_ERROR
            else:
                data = {
                    "id": result
                }

        self.render_json(code=code, data=data)
        return

    def get(self):
        _id = self.get_query_argument('id', None)

        post = post_db.get_post_by_id(id=_id)

        if not post:
            raise HTTPError(404)
        else:
            data = {
                "post": post,
            }

        self.render('post/post.html', data=data)
