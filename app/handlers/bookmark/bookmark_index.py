# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""bookmark index"""


from app.lib.do_cache import do_temp_cache

from app.handlers.base_handler import BaseHandler
from app.handlers.base_handler import authenticated

from app.database.bookmark import bookmark_db


class IndexHandler(BaseHandler):

    """bookmark index handler"""

    # @authenticated
    # @do_temp_cache(60, with_user=False)
    def get(self):
        """bookmark index page"""
        b_type = self.get_query_argument('b_type', None)
        offset = self.get_query_argument('offset', None) or 0
        limit = self.get_query_argument('limit', None) or 20
        # bookmarks = bookmark_db.get_bookmarks(offset=offset, limit=limit)
        bookmarks = bookmark_db.get_sorted_bookmarks_by_rate(offset=offset, limit=limit)
        bookmarks_top10 = bookmark_db.get_sorted_bookmarks_by_rate(offset=0, limit=10)
        if bookmarks:
            result = bookmarks
        else:
            result = []
        data = {
            "bookmarks": result,
            "bookmarks_top10": bookmarks_top10,
        }
        self.render('bookmark/bookmark_index.html', data=data)

    def options(self):
        self.write('GET')
