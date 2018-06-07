# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from handlers.base_handler import BaseHandler
from database.post import post_db


class PostListHandler(BaseHandler):
    """Post list handler"""

    def get(self):
        all_posts = post_db.get_all_posts()

        data = {
            "posts": all_posts,
        }
        self.render('post/post_list.html', data=data)
