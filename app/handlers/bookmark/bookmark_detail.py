# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""bookmark detail handler"""


from app.handlers.base_handler import BaseHandler
from app.handlers.base_handler import authenticated

from app.database.bookmark import bookmark_db

from app.lib.system_code import SUCCESS
from app.lib.system_code import PARAMS_MISS
from app.lib.system_code import ADD_FAILED


class BookmarkDetailHandler(BaseHandler):

    """bookmark detail handler"""

    # @authenticated
    def post(self):
        """bookmark add api"""
        name = self.get_json_argument('name', None)
        url = self.get_json_argument('url', None)
        _type = self.get_json_argument('type', None)
        info = self.get_json_argument('info', None)

        code = SUCCESS
        data = None

        if not all([name, url, _type]):
            code = PARAMS_MISS
        else:
            add_item = {
                "name": name,
                "url": url,
                "type": _type,
                "info": info,
                "creator": self.current_user or 0,
            }
            result = bookmark_db.add_bookmark(item=add_item)
            if not result:
                code = ADD_FAILED
            else:
                data = {
                    "id": result
                }

        self.render_json(code=code, data=data)

    # @authenticated
    def delete(self):
        """bookmark delete api"""
        _id = self.get_query_argument('id', None)

        code = SUCCESS
        data = None

        if not _id:
            code = PARAMS_MISS
        else:
            result = bookmark_db.delete_bookmark(_id=_id)
            if result:
                data = {
                    "result": True,
                }

        self.render_json(code=code, data=data)

    # @authenticated
    def put(self):
        """bookmark update api"""
        _id = self.get_json_argument('id', None)
        name = self.get_json_argument('name', None)
        url = self.get_json_argument('url', None)
        _type = self.get_json_argument('type', None)
        info = self.get_json_argument('info', None)

        code = SUCCESS
        data = None

        if not all([_id, name, url, _type]):
            code = PARAMS_MISS
        else:
            update_item = {
                "name": name,
                "url": url,
                "type": _type,
                "info": info,
            }
            result = bookmark_db.update_bookmark(_id=_id, item=update_item)
            if result:
                data = {
                    "result": True,
                }

        self.render_json(code=code, data=data)

    # @authenticated
    def get(self):
        """bookmark detail page"""
        bookmarks = bookmark_db.get_all_bookmarks()
        if bookmarks:
            result = bookmarks
        else:
            result = []
        data = {
            "bookmarks": result,
        }
        self.render('bookmark/bookmark_detail.html', data=data)

    def options(self):
        self.write('POST,PUT,GET')
