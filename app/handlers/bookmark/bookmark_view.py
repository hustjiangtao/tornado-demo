# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""bookmark view"""


from app.lib.do_cache import do_temp_cache

from app.handlers.base_handler import BaseHandler
from app.handlers.base_handler import authenticated

from app.database.bookmark import bookmark_db


class ViewHandler(BaseHandler):

    """bookmark view handler"""

    # @authenticated
    # @do_temp_cache(60 * 5, with_user=False)
    def get(self):
        """bookmark view page"""
        offset = self.get_query_argument('offset', None) or 0
        limit = self.get_query_argument('limit', None) or 10
        type = self.get_query_argument('type', None)
        bookmarks = bookmark_db.get_bookmarks(offset=offset, limit=limit)
        # bookmarks = bookmark_db.get_sorted_bookmarks_by_rate(offset=offset, limit=limit)
        if bookmarks:
            result = bookmarks
        else:
            result = []
        data = {
            "offset": offset,
            "limit": limit,
            "bookmarks": result,
        }
        if type == 'api':
            self.render_json(code=200, data=data)
        else:
            self.render('bookmark/bookmark_view.html', data=data)

    def options(self):
        self.write('GET')
