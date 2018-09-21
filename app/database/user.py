# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""User"""


from database.base import BaseDB
from database.models import UserModel


class UserDB(BaseDB):
    """用户DB"""

    def add_user(self, item):
        """Add a user
        :param item: {
            'name': 'jiangtao',
            'email': 'jiangtao.hu@qq.com',
            'mobile': '17612141727',
            'password': 'a319c89da307cf078445e00688f903a6d86a7c2cc8d8fd88705db9400c0bcfdd',
            'salt': 'wcmd2s8tau'
            }
        """
        if not isinstance(item, dict):
            return False

        user_model = UserModel()
        user_model.name = item.get('name')
        user_model.email = item.get('email')
        user_model.mobile = item.get('mobile')
        user_model.password = item.get('password')
        user_model.salt = item.get('salt')

        result = self.add(user_model)
        print(result)
        if result:
            result = user_model.id
            print(result)

        return result

    def update_user(self, _id, item):
        """update a user
        :param item: {
            "name": 'jiangtao',
            "email": 'jiangtao.hu@qq.com'
            }
        True
        """
        if not _id or not isinstance(item, dict):
            return False

        query = self.db_session.query(UserModel).filter_by(id=_id)
        user = self.fetch_first(query)
        if not user:
            return False

        user.name = item.get('name')
        user.email = item.get('email')
        user.mobile = item.get('mobile')
        result = self.save(user)

        return result

    def get_user_auth_by_name(self, name):
        """get a user by his name
        :param name: name
        """
        if not name:
            return {}

        query = self.db_session.query(UserModel).filter_by(name=name)
        user = self.fetch_first(query)
        if user:
            result = {
                "id": user.id,
                "password": user.password,
                "salt": user.salt,
            }
        else:
            result = {}

        return result

    def get_user_by_id(self, _id):
        """get a user
        :param _id: id
        """
        if not _id:
            return {}
        if not isinstance(_id, int):
            _id = int(_id)

        query = self.db_session.query(UserModel).filter_by(id=_id)
        user = self.fetch_first(query)
        if user:
            result = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "mobile": user.mobile,
                "create_time": user.create_time,
            }
        else:
            result = {}

        return result


user_db = UserDB()


if __name__ == '__main__':
    user_db = UserDB()
    print(user_db.add_user({
        "name": 'jiangtao',
        "email": 'jiangtao.hu@qq.com',
    }))
