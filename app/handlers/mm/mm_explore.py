# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""mm explore"""


from random import randint

from app.lib.do_cache import do_temp_cache

from app.handlers.base_handler import BaseHandler
from app.handlers.base_handler import authenticated

from app.database.mm import mm_db


class ExploreHandler(BaseHandler):

    """mm explore handler"""

    # @authenticated
    # @do_temp_cache(60 * 5, with_user=False)
    def get(self):
        """mm explore page"""
        offset = self.get_query_argument('offset', None) or 0
        limit = self.get_query_argument('limit', None) or 10
        _type = self.get_query_argument('type', None)
        if int(offset) < 10000:
            offset = randint(0, 100) + int(offset)
        mms = mm_db.get_mms(offset=offset, limit=limit)
        # mms = mm_db.get_sorted_mms_by_rate(offset=offset, limit=limit)
        if mms:
            result = mms
        else:
            result = []
        data = {
            "offset": offset,
            "limit": limit,
            "mms": result,
        }
        if _type == 'api':
            self.render_json(code=200, data=data)
        else:
            self.render('bookmark/mm_explore.html', data=data)

    def options(self):
        self.write('GET')
