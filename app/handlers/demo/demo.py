# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Demo"""


from app.handlers.base_handler import BaseHandler
from app.handlers.base_handler import authenticated

from app.database.demo import demo_db

from app.lib.system_code import SUCCESS
from app.lib.system_code import PARAMS_MISS


class DemoHandler(BaseHandler):

    """A demo handler"""

    @authenticated
    def post(self):
        """demo add api"""
        name = self.get_json_argument('name', None)

        code = SUCCESS
        data = None

        if not name:
            code = PARAMS_MISS
        else:
            add_item = {
                "name": name,
            }
            result = demo_db.add_demo(item=add_item)
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
        _id = self.get_json_argument('id', None)
        name = self.get_json_argument('name', None)

        code = SUCCESS
        data = None

        if not all([_id, name]):
            code = PARAMS_MISS
        else:
            update_item = {
                "name": name,
            }
            result = demo_db.update_demo(_id=_id, item=update_item)
            if result:
                data = {
                    "result": True,
                }

        self.render_json(code=code, data=data)

    @authenticated
    def get(self):
        """demo info page"""
        _id = self.get_json_argument('id', None)
        demo = demo_db.get_demo_by_id(_id=_id)
        if demo:
            demo = {
                "name": demo.get('name') or '',
                "create_time": demo.get('create_time'),
            }
        else:
            demo = {}
        data = {
            "demo": demo,
        }
        self.render('demo/demo.html', data=data)

    @authenticated
    def options(self):
        self.write('POST,PUT,GET')
