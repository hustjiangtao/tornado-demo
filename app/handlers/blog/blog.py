# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Blog page"""


from app.handlers.base_handler import BaseHandler


class BlogHandler(BaseHandler):
    """Blog page handler"""

    def get(self):
        """Blog page"""
        self.render('mdl/blog.html')
