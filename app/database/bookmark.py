# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""bookmark db"""


from datetime import date

from sqlalchemy import desc

from app.database.base import BaseDB
from app.database.models import BookmarkModel
from app.database.models import BookmarkStatsModel


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
        if item.get('info'):
            bookmark_model.info = item.get('info')

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
        bookmark.url = item.get('url')
        bookmark.type = item.get('type')
        bookmark.info = item.get('info')
        if item.get('info'):
            bookmark.info = item.get('info')

        result = self.save(bookmark)

        return result

    def delete_bookmark(self, _id):
        """update a demo
        >>> 1
        True
        """
        if not _id:
            return False

        query = self.db_session.query(BookmarkModel).filter_by(id=_id)
        result = self.delete(query)

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

        query_params=('id', 'name', 'url', 'type', 'info', 'create_time')
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

        query_params = ('id', 'name', 'url', 'type', 'info', 'create_time')
        query = self.db_session.query(BookmarkModel)
        bookmarks = self.fetch_all(query, offset=offset, limit=limit)
        if bookmarks:
            result = [x.to_dict(include=query_params) for x in bookmarks]
        else:
            result = []

        return result

    def get_sorted_bookmarks_by_rate(self, offset=None, limit=None):
        """
        get bookmarks sorted by rate
        :param offset: offset
        :param limit: limit
        :return: list
        """
        if any([offset is None, limit is None]):
            return []

        query_params = ('id', 'name', 'url', 'type', 'info', 'create_time', 'sum_stats')
        query = self.db_session.query(BookmarkModel)
        query = query.outerjoin(BookmarkStatsModel, BookmarkStatsModel.id == BookmarkModel.id)
        query = query.order_by(desc(BookmarkStatsModel.rate), BookmarkModel.id)
        bookmarks = self.fetch_all(query, offset=offset, limit=limit)
        if bookmarks:
            result = [x.to_dict(include=query_params) for x in bookmarks]
        else:
            result = []

        return result

    def get_all_bookmarks(self, offset=None, limit=None):
        """
        get all bookmarks
        :param offset: offset
        :param limit: limit
        :return: list
        """

        query_params = ('id', 'name', 'url', 'type', 'info', 'create_time')
        query = self.db_session.query(BookmarkModel)
        bookmarks = self.fetch_all(query, offset=offset, limit=limit)
        if bookmarks:
            result = [x.to_dict(include=query_params) for x in bookmarks]
        else:
            result = []

        return result

    def increase_bookmark_click(self, _id):
        """Add a demo
        :param _id: bookmark id
        >>> 1
        True
        """
        if not _id:
            return False

        query = self.db_session.query(BookmarkStatsModel)
        query = query.filter_by(id=_id)
        stat = self.fetch_first(query)
        if stat:
            stat.click += 1
            result = self.save(stat)
        else:
            stat_model = BookmarkStatsModel()
            stat_model.id = _id
            stat_model.click = 1

            result = self.add(stat_model)

        return result


bookmark_db = BookmarkDB()


if __name__ == '__main__':
    bookmark_db = BookmarkDB()
    print(bookmark_db.get_bookmarks())
