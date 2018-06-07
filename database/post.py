# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from datetime import datetime
from database.base import BaseDB


class PostDB(BaseDB):
    """Post DB"""

    def add_post(self, item):
        """Add a post
        >>> {"title": 'jiangtao-first-post', "content": 'my email is jiangtao.hu@qq.com', "author": 'jiangtao'}
        True
        """
        if not isinstance(item, dict):
            return False

        sql = "insert into post (title, content, author) values (:title, :content, :author);"
        result = self.add_item(insert_sql=sql, params=item)
        if result:
            return result
        else:
            return False

    def get_post_by_id(self, id):
        """get a post by it's id
        >>> 1
        True
        """
        if not id:
            return {}

        sql = "select * from post where id = {id}".format(id=id)
        result = self.fetch_one(sql)
        if result:
            _id, title, content, author, create_time = result
            result = {
                "id": _id,
                "title": title,
                "content": content,
                "author": author,
                "create_time": datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S"),
            }
        else:
            result = {}

        return result

    def get_all_posts(self):
        """get all posts
        >>>
        True
        """
        sql = "select * from post where 1"
        result = self.fetch_all(sql)
        if result:
            result = [{
                "id": _id,
                "title": title,
                "content": content,
                "author": author,
                "create_time": datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S"),
            } for _id, title, content, author, create_time in result]
        else:
            result = []

        return result


post_db = PostDB()


if __name__ == '__main__':
    post_db = PostDB()
    print(post_db.add_post({
        "title": 'jiangtao-first-post',
        "content": 'my email is jiangtao.hu@qq.com',
        "author": 'jiangtao'
    }))
