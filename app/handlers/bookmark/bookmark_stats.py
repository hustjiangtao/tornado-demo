# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""bookmark stats click handler"""


from tornado import gen

from app.handlers.base_handler import BaseHandler

from app.database.bookmark import bookmark_db

from app.lib.system_code import SUCCESS
from app.lib.system_code import PARAMS_MISS


class ClickHandler(BaseHandler):

    """bookmark stats click handler"""

    @gen.coroutine
    def get(self):
        """bookmark stats click"""
        _id = self.get_query_argument('id', None)

        code = SUCCESS
        data = None

        if not _id:
            code = PARAMS_MISS
        else:
            result = bookmark_db.increase_bookmark_click(bid=_id)
            data = {
                "result": result,
            }

        self.render_json(code=code, data=data)

    def options(self):
        self.write('GET')
