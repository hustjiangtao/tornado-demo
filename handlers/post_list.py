# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import random

from handlers.base_handler import BaseHandler
from database.post import post_db


class PostListHandler(BaseHandler):
    """Post list handler"""

    def get(self):
        search = self.get_query_argument('search', None)
        offset = random.randint(0, 100)
        limit = 20
        all_posts = post_db.get_all_posts(offset=offset, limit=limit, search=search)

        data = {
            "offset": offset,
            "limit": limit,
            "search": search,
            "posts": all_posts,
        }
        self.render('post/post_list.html', data=data)
