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


user_db = UserDB()


if __name__ == '__main__':
    user_db = UserDB()
    print(user_db.add_user({
        "name": 'jiangtao',
        "email": 'jiangtao.hu@qq.com',
    }))
