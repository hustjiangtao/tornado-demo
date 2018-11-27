# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""mv db"""


from datetime import date

from sqlalchemy import desc

from app.database.base import BaseDB
from app.database.models import MvModel
from app.database.models import MvStatsModel


class MvDB(BaseDB):
    """MvDB"""

    def add_mv(self, item):
        """Add a demo
        >>> {'name': 'jiangtao'}
        int
        """
        if not isinstance(item, dict):
            return False

        mv_model = MvModel()
        mv_model.name = item.get('name')
        mv_model.url = item.get('url')
        mv_model.cover_url = item.get('cover_url')
        mv_model.type = item.get('type')
        mv_model.creator = item.get('creator')
        mv_model.source = item.get('source')
        if item.get('ori_url'):
            mv_model.ori_url = item.get('ori_url')
        if item.get('info'):
            mv_model.info = item.get('info')
        if item.get('download_url'):
            mv_model.download_url = item.get('download_url')
        if item.get('duration'):
            mv_model.duration = item.get('duration')
        if item.get('size'):
            mv_model.size = item.get('size')
        if item.get('width'):
            mv_model.width = item.get('width')
        if item.get('height'):
            mv_model.height = item.get('height')

        result = self.add(mv_model)
        if result:
            result = mv_model.id

        return result

    def add_many_mvs(self, items):
        """Add many demos
        >>> [{'name': 'jiangtao'}]
        bool
        """
        if not isinstance(items, list):
            return False

        add_items = []
        for item in items:
            mv_model = MvModel()
            mv_model.name = item.get('name')
            mv_model.url = item.get('url')
            mv_model.cover_url = item.get('cover_url')
            mv_model.type = item.get('type')
            mv_model.creator = item.get('creator')
            mv_model.source = item.get('source')
            if item.get('ori_url'):
                mv_model.ori_url = item.get('ori_url')
            if item.get('info'):
                mv_model.info = item.get('info')
            if item.get('download_url'):
                mv_model.download_url = item.get('download_url')
            if item.get('duration'):
                mv_model.duration = item.get('duration')
            if item.get('size'):
                mv_model.size = item.get('size')
            if item.get('width'):
                mv_model.width = item.get('width')
            if item.get('height'):
                mv_model.height = item.get('height')
            add_items.append(mv_model)

        result = self.add_all(add_items)

        return result

    def update_mv(self, _id, item):
        """update a demo
        >>> {"name": 'jiangtao'}
        True
        """
        if not _id or not isinstance(item, dict):
            return False

        query = self.db_session.query(MvModel).filter_by(id=_id)
        mv = self.fetch_first(query)
        if not mv:
            return False

        mv.name = item.get('name')
        mv.type = item.get('type')
        mv.info = item.get('info')
        if item.get('info'):
            mv.info = item.get('info')

        result = self.save(mv)

        return result

    def delete_mv(self, _id):
        """delete a demo
        >>> 1
        True
        """
        if not _id:
            return False

        query = self.db_session.query(MvModel).filter_by(id=_id)
        result = self.delete(query)

        return result

    def get_mv_by_id(self, _id):
        """
        get a mv by id
        :param _id: mv id
        :return: dict
        """
        if not _id:
            return {}
        if not isinstance(_id, int):
            _id = int(_id)

        # query_params = ('id', 'name', 'url', 'type', 'info', 'source', 'create_time')
        query = self.db_session.query(MvModel).filter_by(id=_id)
        mv = self.fetch_first(query)
        if mv:
            # result = mv.to_dict(include=query_params)
            result = mv.to_dict()
        else:
            result = {}

        return result

    def get_mvs(self, offset=None, limit=None):
        """
        get mvs
        :param offset: offset
        :param limit: limit
        :return: list
        """
        if any([offset is None, limit is None]):
            return []

        # query_params = ('id', 'name', 'url', 'type', 'info', 'source', 'create_time')
        query = self.db_session.query(MvModel)
        mvs = self.fetch_all(query, offset=offset, limit=limit)
        if mvs:
            # result = [x.to_dict(include=query_params) for x in mms]
            result = [x.to_dict() for x in mvs]
        else:
            result = []

        return result

    def get_sorted_mvs_by_rate(self, offset=None, limit=None):
        """
        get mvs sorted by rate
        :param offset: offset
        :param limit: limit
        :return: list
        """
        if any([offset is None, limit is None]):
            return []

        # query_params = ('id', 'name', 'url', 'type', 'info', 'source', 'create_time', 'sum_stats')
        query = self.db_session.query(MvModel)
        query = query.outerjoin(MvStatsModel, MvStatsModel.id == MvModel.id)
        query = query.order_by(desc(MvStatsModel.rate), MvModel.id)
        mvs = self.fetch_all(query, offset=offset, limit=limit)
        if mvs:
            # result = [x.to_dict(include=query_params) for x in mvs]
            result = [x.to_dict() for x in mvs]
        else:
            result = []

        return result

    def get_all_mvs(self, offset=None, limit=None):
        """
        get all mvs
        :param offset: offset
        :param limit: limit
        :return: list
        """

        # query_params = ('id', 'name', 'url', 'type', 'info', 'source', 'create_time')
        query = self.db_session.query(MvModel)
        mvs = self.fetch_all(query, offset=offset, limit=limit)
        if mvs:
            # result = [x.to_dict(include=query_params) for x in mvs]
            result = [x.to_dict() for x in mvs]
        else:
            result = []

        return result

    def increase_mv_click(self, _id):
        """Add a demo
        :param _id: mv id
        >>> 1
        True
        """
        if not _id:
            return False

        query = self.db_session.query(MvStatsModel)
        query = query.filter_by(id=_id)
        stat = self.fetch_first(query)
        if stat:
            stat.click += 1
            result = self.save(stat)
        else:
            stat_model = MvStatsModel()
            stat_model.id = _id
            stat_model.click = 1

            result = self.add(stat_model)

        return result


mv_db = MvDB()


if __name__ == '__main__':
    mv_db = MvDB()
    print(mv_db.get_mvs())
