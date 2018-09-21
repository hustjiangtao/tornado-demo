# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Post"""


from tornado.web import HTTPError

from app.handlers.base_handler import BaseHandler
from app.handlers.base_handler import authenticated

from app.database.post import post_db
from app.database.user import user_db

from app.lib.system_code import SUCCESS
from app.lib.system_code import PARAMS_MISS
from app.lib.system_code import POST_ADD_ERROR


class PostHandler(BaseHandler):
    """Post handler"""

    @authenticated
    def post(self):
        title = self.get_json_argument('title', None)
        intro = self.get_json_argument('intro', None)
        content = self.get_json_argument('content', None)
        format_ = self.get_json_argument('format', None)

        code = SUCCESS
        data = None

        if not all([title, content]):
            code = PARAMS_MISS
        else:
            current_user = user_db.get_user_by_id(_id=self.current_user)
            add_item = {
                "title": title,
                "author": current_user.get('name'),
                "intro": intro,
                "content": content,
                "format": format_,
            }
            result = post_db.add_post(item=add_item)
            if not result:
                code = POST_ADD_ERROR
            else:
                data = {
                    "id": result
                }

        self.render_json(code=code, data=data)

    @authenticated
    def put(self):
        _id = self.get_json_argument('id', None)
        title = self.get_json_argument('title', None)
        intro = self.get_json_argument('intro', None)
        content = self.get_json_argument('content', None)
        format_ = self.get_json_argument('format', None)

        code = SUCCESS
        data = None

        if not all([title, intro, content, format_]):
            code = PARAMS_MISS
        else:
            update_item = {
                "id": _id,
                "title": title,
                "intro": intro,
                "content": content,
                "format": format_,
            }
            result = post_db.update_post(_id=_id, item=update_item)
            if not result:
                code = POST_ADD_ERROR
            else:
                data = {
                    "id": result
                }

        self.render_json(code=code, data=data)

    @authenticated
    def get(self):
        _id = self.get_query_argument('id', None)

        post = post_db.get_post_by_id(_id=_id)

        if not _id:
            data = None
        elif not post:
            raise HTTPError(404)
        else:
            data = {
                "post": post,
            }

        self.render('post/post.html', data=data)
