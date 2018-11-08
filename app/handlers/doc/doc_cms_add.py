# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Doc CMS"""


from app.handlers.base_handler import BaseHandler
from app.handlers.base_handler import authenticated
from app.lib.do_cache import do_temp_cache

from app.database.doc import doc_db

from app.lib.system_code import SUCCESS
from app.lib.system_code import PARAMS_MISS

from app.scripts.convert_md.convert_md import convert_md


class DocCMSAddHandler(BaseHandler):

    """doc cms add handler"""

    # @authenticated
    def post(self):
        """doc add api"""
        title = self.get_body_argument('title', None)
        category = self.get_body_argument('category', None)
        tags = self.get_body_argument('tags', None)
        content = self.get_body_argument('content', None)
        print(title)

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
        pass

    # @authenticated
    # @do_temp_cache(7*3600, with_user=False)
    def get(self):
        """detail info page"""
        self.render('mdl/doc_cms_add.html')

    # @authenticated
    def options(self):
        self.write('POST,GET')
