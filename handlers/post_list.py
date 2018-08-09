# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Post list"""


import random

from handlers.base_handler import BaseHandler
from database.post import post_db
from lib.utils import json_encode, json_decode


class PostListHandler(BaseHandler):
    """Post list handler"""

    def get(self):
        search = self.get_query_argument('search', None)
        offset = random.randint(0, 100)
        limit = 20
        all_posts = json_decode(self.r.get(name=self.request.uri))
        cached = True if all_posts else False
        if not all_posts:
            all_posts = post_db.get_all_posts(offset=offset, limit=limit, search=search)
            if all_posts:
                self.r.setex(name=self.request.uri, value=json_encode(all_posts), time=60)

        data = {
            "offset": offset,
            "limit": limit,
            "search": search,
            "posts": all_posts,
            "cached": cached,
        }
        self.render('post/post_list.html', data=data)
