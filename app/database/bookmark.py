# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""bookmark db"""


from app.database.base import BaseDB
from app.database.models import BookmarkModel


class BookmarkDB(BaseDB):
    """用户DB"""

    def add_bookmark(self, item):
        """Add a demo
        >>> {'name': 'jiangtao'}
        int
        """
        if not isinstance(item, dict):
            return False

        bookmark_model = BookmarkModel()
        bookmark_model.name = item.get('name')
        bookmark_model.url = item.get('url')
        bookmark_model.type = item.get('type')
        bookmark_model.creator = item.get('creator')

        result = self.add(bookmark_model)
        if result:
            result = bookmark_model.id

        return result

    def update_bookmark(self, _id, item):
        """update a demo
        >>> {"name": 'jiangtao'}
        True
        """
        if not _id or not isinstance(item, dict):
            return False

        query = self.db_session.query(BookmarkModel).filter_by(id=_id)
        bookmark = self.fetch_first(query)
        if not bookmark:
            return False

        bookmark.name = item.get('name')
        result = self.save(bookmark)

        return result

    def get_bookmark_by_id(self, _id):
        """
        get a bookmark by id
        :param _id: bookmark id
        :return: dict
        """
        if not _id:
            return {}
        if not isinstance(_id, int):
            _id = int(_id)

        query_params=('id', 'name', 'url', 'type', 'create_time')
        query = self.db_session.query(BookmarkModel).filter_by(id=_id)
        bookmark = self.fetch_first(query)
        if bookmark:
            result = bookmark.to_dict(include=query_params)
        else:
            result = {}

        return result

    def get_bookmarks(self, offset=None, limit=None):
        """
        get bookmarks
        :param offset: offset
        :param limit: limit
        :return: list
        """
        if any([offset is None, limit is None]):
            return []

        query_params = ('id', 'name', 'url', 'type', 'create_time')
        query = self.db_session.query(BookmarkModel)
        bookmarks = self.fetch_all(query, offset=offset, limit=limit)
        if bookmarks:
            result = [x.to_dict(include=query_params) for x in bookmarks]
        else:
            result = []

        return result


bookmark_db = BookmarkDB()


if __name__ == '__main__':
    bookmark_db = BookmarkDB()
    print(bookmark_db.get_bookmarks())
