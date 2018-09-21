# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Demo"""


from app.database.base import BaseDB
from app.database.models import DemoModel


class DemoDB(BaseDB):
    """用户DB"""

    def add_demo(self, item):
        """Add a demo
        >>> {'name': 'jiangtao'}
        int
        """
        if not isinstance(item, dict):
            return False

        demo_model = DemoModel()
        demo_model.name = item.get('name')

        result = self.add(demo_model)
        if result:
            result = demo_model.id

        return result

    def update_demo(self, _id, item):
        """update a demo
        >>> {"name": 'jiangtao'}
        True
        """
        if not _id or not isinstance(item, dict):
            return False

        query = self.db_session.query(DemoModel).filter_by(id=_id)
        demo = self.fetch_first(query)
        if not demo:
            return False

        demo.name = item.get('name')
        result = self.save(demo)

        return result

    def get_demo_by_id(self, _id):
        """get a demo
        >>> 1
        {}
        """
        if not _id:
            return {}
        if not isinstance(_id, int):
            _id = int(_id)

        query = self.db_session.query(DemoModel).filter_by(id=_id)
        demo = self.fetch_first(query)
        if demo:
            result = {
                "id": demo.id,
                "name": demo.name,
                "create_time": demo.create_time,
            }
        else:
            result = {}

        return result


demo_db = DemoDB()


if __name__ == '__main__':
    demo_db = DemoDB()
    print(demo_db.get_demo_by_id(1))
