# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


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

        sql = "insert into user (name, email) values (:name, :email);"
        result = self.add_item(insert_sql=sql, params=item)
        if result:
            return True
        else:
            return False

    def get_user_by_name(self, name):
        """get a user by his name
        >>> 'jiangtao'
        True
        """
        if not name:
            return False

        sql = "select id, name, email from user where name = '{name}'".format(name=name)
        result = self.fetch_one(sql)
        if result:
            _id, name, email = result
            result = {
                "id": _id,
                "name": name,
                "email": email,
            }
        else:
            result = None

        return result

    def get_user_by_id(self, id):
        """get a user
        >>> 'jiangtao'
        True
        """
        if not id:
            return False

        sql = "select * from user where id = '{id}'".format(id=id)
        result = self.fetch_one(sql)
        if result:
            _id, name, email, mobile, create_time = result
            result = {
                "id": _id,
                "name": name,
                "email": email,
                "mobile": mobile,
                "create_time": create_time,
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
