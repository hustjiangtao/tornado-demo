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

        code = SUCCESS
        data = None

        if not all([name, url, _type]):
            code = PARAMS_MISS
        else:
            add_item = {
                "name": name,
                "url": url,
                "type": _type,
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
        pass

    # @authenticated
    def put(self):
        """bookmark update api"""
        _id = self.get_json_argument('id', None)
        name = self.get_json_argument('name', None)
        url = self.get_json_argument('url', None)
        _type = self.get_json_argument('type', None)

        code = SUCCESS
        data = None

        if not all([_id, name, url, _type]):
            code = PARAMS_MISS
        else:
            update_item = {
                "name": name,
                "url": url,
                "type": _type,
            }
            result = bookmark_db.update_bookmark(_id=_id, item=update_item)
            if result:
                data = {
                    "result": True,
                }

        self.render_json(code=code, data=data)

    # @authenticated
    def get(self, _id):
        """bookmark detail page"""
        bookmark = bookmark_db.get_bookmark_by_id(_id=_id)
        if bookmark:
            result = bookmark
        else:
            result = {}
        data = {
            "bookmark": result,
        }
        self.render('bookmark/bookmark_detail.html', data=data)

    def options(self):
        self.write('POST,PUT,GET')
