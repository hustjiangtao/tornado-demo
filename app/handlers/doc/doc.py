# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Doc"""


from app.handlers.base_handler import BaseHandler
from app.handlers.base_handler import authenticated
from app.lib.do_cache import do_temp_cache

from app.database.doc import doc_db

from app.lib.system_code import SUCCESS
from app.lib.system_code import PARAMS_MISS

from app.scripts.convert_md.convert_md import convert_md


class DocHandler(BaseHandler):

    """doc handler"""

    @authenticated
    def post(self):
        """doc add api"""
        title = self.get_body_argument('title', None)
        category = self.get_body_argument('category', None)
        tags = self.get_body_argument('tags', None)
        content = self.get_body_argument('content', None)

        code = SUCCESS
        data = None

        if not all([title, category, content]):
            code = PARAMS_MISS
        else:
            if tags:
                tags = tags.strip()
            add_item = {
                "title": title,
                "category": category,
                "tags": tags,
                "content": content,
            }
            result = doc_db.add_doc(item=add_item)
            if result:
                data = {
                    "id": result,
                }

        self.render_json(code=code, data=data)

    @authenticated
    def delete(self):
        pass

    @authenticated
    def put(self):
        """demo update api"""
        _id = self.get_body_argument('id', None)
        title = self.get_body_argument('title', None)
        category = self.get_body_argument('category', None)
        tags = self.get_body_argument('tags', None)
        content = self.get_body_argument('content', None)

        code = SUCCESS
        data = None

        if not all([_id, title, category, content]):
            code = PARAMS_MISS
        else:
            if tags:
                tags = tags.strip()
            update_item = {
                "title": title,
                "category": category,
                "tags": tags,
                "content": content,
            }
            result = doc_db.update_doc(_id=_id, item=update_item)
            if result:
                data = {
                    "result": True,
                }

        self.render_json(code=code, data=data)

    # @authenticated
    @do_temp_cache(7*3600, with_user=False)
    def get(self, _id):
        """detail info page"""
        item = doc_db.get_doc_by_id(_id=_id)
        if item:
            item = {
                "title": item.get('title') or '',
                "author": item.get('author') or '',
                "category": item.get('category') or '',
                "tags": item.get('tags') or '',
                "content": convert_md(item.get('content') or ''),
                "read_count": item.get('read_count') or 0,
            }
        else:
            item = {}
        data = {
            "item": item,
        }
        self.render('mdl/doc_detail.html', data=data)

    # @authenticated
    def options(self):
        self.write('POST,PUT,GET')
