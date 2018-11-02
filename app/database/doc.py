# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Doc"""


from sqlalchemy import desc

from app.database.base import BaseDB
from app.database.models import DocModel


class DocDB(BaseDB):
    """文档DB"""

    def add_doc(self, item):
        """Add a item
        >>> {'name': 'jiangtao'}
        int
        """
        if not isinstance(item, dict):
            return False

        model = DocModel()
        model.title = item.get('title')
        model.category = item.get('category')
        model.tag = item.get('tag')
        model.content = item.get('content')
        if item.get('author'):
            model.author = item.get('author')

        result = self.add(model)
        if result:
            result = model.id

        return result

    def update_doc(self, _id, item):
        """update a item
        >>> {"name": 'jiangtao'}
        True
        """
        if not _id or not isinstance(item, dict):
            return False

        query = self.db_session.query(DocModel).filter_by(id=_id)
        item = self.fetch_first(query)
        if not item:
            return False

        item.title = item.get('title')
        item.category = item.get('category')
        item.tag = item.get('tag')
        item.content = item.get('content')
        result = self.save(item)

        return result

    def delete_doc(self, _id):
        """delete a item
        >>> 1
        True
        """
        if not _id:
            return False

        query = self.db_session.query(DocModel).filter_by(id=_id)
        result = self.delete(query)

        return result

    def get_doc_by_id(self, _id):
        """
        get a item by id
        :param _id: item id
        :return: dict
        """
        if not _id:
            return {}
        if not isinstance(_id, int):
            _id = int(_id)

        query_params = ('id', 'title', 'author', 'category', 'tag', 'content', 'status', 'read_count', 'update_time')
        query = self.db_session.query(DocModel).filter_by(id=_id)
        item = self.fetch_first(query)
        if item:
            result = item.to_dict(include=query_params)
        else:
            result = {}

        return result

    def get_docs(self, offset=None, limit=None):
        """
        get items
        :param offset: offset
        :param limit: limit
        :return: list
        """
        if any([offset is None, limit is None]):
            return []

        query_params = ('id', 'title', 'author', 'category', 'tag', 'content', 'status', 'read_count', 'update_time')
        query = self.db_session.query(DocModel)
        items = self.fetch_all(query, offset=offset, limit=limit)
        if items:
            result = [x.to_dict(include=query_params) for x in items]
        else:
            result = []

        return result

    def get_sorted_docs_by_read(self, offset=None, limit=None):
        """
        get items sorted by read
        :param offset: offset
        :param limit: limit
        :return: list
        """
        if any([offset is None, limit is None]):
            return []

        query_params = ('id', 'title', 'author', 'category', 'tag', 'content', 'status', 'read_count', 'update_time')
        query = self.db_session.query(DocModel)
        query = query.order_by(desc(DocModel.read_count), DocModel.id)
        items = self.fetch_all(query, offset=offset, limit=limit)
        if items:
            result = [x.to_dict(include=query_params) for x in items]
        else:
            result = []

        return result

    def increase_doc_read(self, _id):
        """increase item read count
        :param _id: item id
        >>> 1
        True
        """
        if not _id:
            return False

        query = self.db_session.query(DocModel)
        query = query.filter_by(id=_id)
        item = self.fetch_first(query)
        if not item:
            return False

        item.click += 1
        result = self.save(item)

        return result


doc_db = DocDB()


if __name__ == '__main__':
    doc_db = DocDB()
    print(doc_db.get_doc_by_id(1))
