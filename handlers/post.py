# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado import gen

from handlers.base_handler import BaseHandler
from handlers.base_handler import authenticated

from lib.system_code import SUCCESS
from lib.system_code import PARAMS_ERROR

from database.service.post_service import get_all_posts
from database.service.post_service import get_post_by_id


class PostHandler(BaseHandler):
    """Post handler"""

    @authenticated
    @gen.coroutine
    def post(self):
        account = self.get_body_argument('account', None)

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
    def delete(self):
        post_id = self.get_body_argument('post_id', None)

        code = SUCCESS
        data = None

        if not post_id:
            code = PARAMS_ERROR
        else:
            data = True

        self.render_json(code=code, data=data)
        return

    @authenticated
    @gen.coroutine
    def put(self):
        post_id = self.get_body_argument('post_id', None)

        code = SUCCESS
        data = None

        if not post_id:
            code = PARAMS_ERROR
        else:
            data = True

        self.render_json(code=code, data=data)
        return

    @gen.coroutine
    def get(self):
        post_id = self.get_query_argument('post_id', None)
        get_type = self.get_query_argument('get_type', None)

        code = SUCCESS
        data = None

        if not any([post_id, get_type]):
            code = PARAMS_ERROR
        else:
            if get_type == 'all':
                all_posts = yield get_all_posts()
                if all_posts:
                    data = [{
                        "id": post.get('id'),
                        "title": post.get('title'),
                        "content": post.get('content'),
                        "tag": post.get('tag'),
                    } for post in all_posts]
            else:
                post = yield get_post_by_id(_id=post_id)
                if post:
                    data = {
                        "id": post.get('id'),
                        "title": post.get('title'),
                        "content": post.get('content'),
                        "tag": post.get('tag'),
                    }

        self.render_json(code=code, data=data)
        return
