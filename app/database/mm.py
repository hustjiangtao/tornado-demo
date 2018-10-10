# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""mm db"""


from datetime import date

from sqlalchemy import desc

from app.database.base import BaseDB
from app.database.models import MmModel
from app.database.models import MmStatsModel


class MmDB(BaseDB):
    """MmDB"""

    def add_mm(self, item):
        """Add a demo
        >>> {'name': 'jiangtao'}
        int
        """
        if not isinstance(item, dict):
            return False

        mm_model = MmModel()
        mm_model.name = item.get('name')
        mm_model.url = item.get('url')
        mm_model.type = item.get('type')
        mm_model.creator = item.get('creator')
        mm_model.source = item.get('source')
        if item.get('ori_url'):
            mm_model.ori_url = item.get('ori_url')
        if item.get('info'):
            mm_model.info = item.get('info')

        result = self.add(mm_model)
        if result:
            result = mm_model.id

        return result

    def update_mm(self, _id, item):
        """update a demo
        >>> {"name": 'jiangtao'}
        True
        """
        if not _id or not isinstance(item, dict):
            return False

        query = self.db_session.query(MmModel).filter_by(id=_id)
        mm = self.fetch_first(query)
        if not mm:
            return False

        mm.name = item.get('name')
        mm.url = item.get('url')
        mm.type = item.get('type')
        if item.get('info'):
            mm.info = item.get('info')

        result = self.save(mm)

        return result

    def delete_mm(self, _id):
        """delete a demo
        >>> 1
        True
        """
        if not _id:
            return False

        query = self.db_session.query(MmModel).filter_by(id=_id)
        result = self.delete(query)

        return result

    def get_mm_by_id(self, _id):
        """
        get a mm by id
        :param _id: mm id
        :return: dict
        """
        if not _id:
            return {}
        if not isinstance(_id, int):
            _id = int(_id)

        query_params=('id', 'name', 'url', 'type', 'info', 'source', 'create_time')
        query = self.db_session.query(MmModel).filter_by(id=_id)
        mm = self.fetch_first(query)
        if mm:
            result = mm.to_dict(include=query_params)
        else:
            result = {}

        return result

    def get_mms(self, offset=None, limit=None):
        """
        get mms
        :param offset: offset
        :param limit: limit
        :return: list
        """
        if any([offset is None, limit is None]):
            return []

        query_params = ('id', 'name', 'url', 'type', 'info', 'source', 'create_time')
        query = self.db_session.query(MmModel)
        mms = self.fetch_all(query, offset=offset, limit=limit)
        if mms:
            result = [x.to_dict(include=query_params) for x in mms]
        else:
            result = []

        return result

    def get_sorted_mms_by_rate(self, offset=None, limit=None):
        """
        get mms sorted by rate
        :param offset: offset
        :param limit: limit
        :return: list
        """
        if any([offset is None, limit is None]):
            return []

        query_params = ('id', 'name', 'url', 'type', 'info', 'source', 'create_time', 'sum_stats')
        query = self.db_session.query(MmModel)
        query = query.outerjoin(MmStatsModel, MmStatsModel.id == MmModel.id)
        query = query.order_by(desc(MmStatsModel.rate), MmModel.id)
        mms = self.fetch_all(query, offset=offset, limit=limit)
        if mms:
            result = [x.to_dict(include=query_params) for x in mms]
        else:
            result = []

        return result

    def get_all_mms(self, offset=None, limit=None):
        """
        get all mms
        :param offset: offset
        :param limit: limit
        :return: list
        """

        query_params = ('id', 'name', 'url', 'type', 'info', 'source', 'create_time')
        query = self.db_session.query(MmModel)
        mms = self.fetch_all(query, offset=offset, limit=limit)
        if mms:
            result = [x.to_dict(include=query_params) for x in mms]
        else:
            result = []

        return result

    def increase_mm_click(self, _id):
        """Add a demo
        :param _id: mm id
        >>> 1
        True
        """
        if not _id:
            return False

        query = self.db_session.query(MmStatsModel)
        query = query.filter_by(id=_id)
        stat = self.fetch_first(query)
        if stat:
            stat.click += 1
            result = self.save(stat)
        else:
            stat_model = MmStatsModel()
            stat_model.id = _id
            stat_model.click = 1

            result = self.add(stat_model)

        return result


mm_db = MmDB()


if __name__ == '__main__':
    mm_db = MmDB()
    print(mm_db.get_mms())
