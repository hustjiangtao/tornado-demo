# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Contact page"""


from handlers.base_handler import BaseHandler


class ContactHandler(BaseHandler):
    """Contact page handler"""

    def get(self):
        """Contact page"""
        self.render('mdl/contact.html')
