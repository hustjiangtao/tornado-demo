# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from datetime import datetime
from database.base import BaseDB


class UserDB(BaseDB):
    """用户DB"""

    def add_user(self, item):
        """Add a user
        >>> {"name": 'jiangtao', "email": 'jiangtao.hu@qq.com'}
        True
        """
        if not isinstance(item, dict):
            return False

        sql = "insert into user (name, email, mobile, password, salt) values (:name, :email, :mobile, :password, :salt);"
        result = self.add_item(insert_sql=sql, params=item)
        if result:
            return result
        else:
            return False

    def update_user(self, item):
        """update a user
        >>> {"name": 'jiangtao', "email": 'jiangtao.hu@qq.com'}
        True
        """
        if not isinstance(item, dict):
            return False

        sql = "update user set name=:name, email=:email, mobile=:mobile where id=:id;"
        result = self.update_item(sql=sql, params=item)
        if result:
            return True
        else:
            return False

    def get_user_auth_by_name(self, name):
        """get a user by his name
        >>> 'jiangtao'
        True
        """
        if not name:
            return False

        sql = "select id, password, salt from user where name = '{name}'".format(name=name)
        result = self.fetch_one(sql)
        if result:
            x = result
            result = {
                "id": x['id'],
                "password": x['password'],
                "salt": x['salt'],
            }
        else:
            result = {}

        return result

    def get_user_by_id(self, id):
        """get a user
        >>> 'jiangtao'
        True
        """
        if not id:
            return False
        elif not isinstance(id, int):
            id = int(id)

        sql = "select * from user where id = {id}".format(id=id)
        result = self.fetch_one(sql)
        if result:
            x = result
            result = {
                "id": x['id'],
                "name": x['name'],
                "email": x['email'],
                "mobile": x['mobile'],
                "create_time": datetime.strptime(x['create_time'], "%Y-%m-%d %H:%M:%S"),
            }
        else:
            result = None

        return result


user_db = UserDB()


if __name__ == '__main__':
    user_db = UserDB()
    print(user_db.add_user({
        "name": 'jiangtao',
        "email": 'jiangtao.hu@qq.com',
    }))
