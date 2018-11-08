# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Doc"""


from collections import defaultdict

from app.handlers.base_handler import BaseHandler
from app.lib.do_cache import do_temp_cache

from app.database.user import user_db
from app.database.doc import doc_db


class DocIndexHandler(BaseHandler):

    """doc handler"""

    # @do_temp_cache(3600, with_user=False)
    def get(self):
        """doc index page"""
        offset = self.get_query_argument('offset', None) or 0
        limit = self.get_query_argument('limit', None) or 100

        docs = doc_db.get_sorted_docs_by_read(offset=offset, limit=limit)
        user_ids = {x.get('author') for x in docs}
        users = user_db.get_users_by_ids(ids=user_ids)
        user_name_dict = {x.get('id'): x.get('name') for x in users}
        items_dict = defaultdict(list)
        if docs:
            for x in docs:
                x['author'] = user_name_dict.get(x.get('author')) or '无名达人'
                items_dict[x.get('category')].append(x)
            result = dict(sorted(items_dict.items(), key=lambda x: x[0]))
        else:
            result = {}

        data = {
            "offset": offset,
            "limit": limit,
            "items": result,
        }
        self.render('mdl/doc_index.html', data=data)

    def options(self):
        self.write('GET')
