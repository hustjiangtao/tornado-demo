# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""About page"""


from handlers.base_handler import BaseHandler


class AboutHandler(BaseHandler):
    """About page handler"""

    def get(self):
        """About page"""
        self.render('mdl/about.html')
