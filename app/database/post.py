# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Post"""


from sqlalchemy import or_

from app.database.base import BaseDB
from app.database.models import PostModel


class PostDB(BaseDB):
    """Post DB"""

    def add_post(self, item):
        """Add a post
        :param item: {
            "title": 'jiangtao-first-post',
            "author": 'jiangtao',
            "intro": 'my email',
            "content": 'my email is jiangtao.hu@qq.com',
            "format": 'markdown',
            }
        """
        if not isinstance(item, dict):
            return False

        post = PostModel()
        post.title = item.get('title')
        post.author = item.get('author')
        post.intro = item.get('intro')
        post.content = item.get('content')
        post.format = item.get('format')

        result = self.add(post)
        if result:
            result = post.id

        return result

    def add_crawler_posts(self, items):
        """Add a post
        :param item: {
            "title": 'jiangtao-first-post',
            "author": 'jiangtao',
            "intro": 'my email',
            "content": 'my email is jiangtao.hu@qq.com',
            "format": 'markdown',
            "source": 'post',
            "source": 'post',
            "source_id": 'source_id',
            "original_url": 'original_url',
            "source_id": 'source_id',
            }
        """
        if not isinstance(items, list):
            return False

        post_models = []
        for item in items:
            post = PostModel()
            post.title = item.get('title')
            post.author = item.get('author')
            post.intro = item.get('intro')
            post.content = item.get('content')
            post.format = item.get('format')
            post.source = item.get('source')
            post.source_id = item.get('source_id')
            post.original_url = item.get('original_url')
            if item.get('create_time'):
                post.create_time = item.get('create_time')

            post_models.append(post)

        result = self.add_all(post_models)
        if result:
            result = True

        return result

    def update_post(self, _id, item):
        """update a post
        :param _id: id
        :param item: {
            "title": 'jiangtao-first-post',
            "intro": 'my email',
            "content": 'my email is jiangtao.hu@qq.com',
            "format": 'markdown',
            }
        """
        if not _id or not isinstance(item, dict):
            return False

        query = self.db_session.query(PostModel).filter_by(id=_id)
        post = self.fetch_first(query)
        if not post:
            return False

        post.title = item.get('title')
        post.intro = item.get('intro')
        post.content = item.get('content')
        post.format = item.get('format')
        result = self.save(post)

        return result

    def get_post_by_id(self, _id):
        """get a post by it's id
        :param _id: id
        """
        if not _id:
            return {}

        query = self.db_session.query(PostModel).filter_by(id=_id)
        post = self.fetch_first(query)
        if post:
            result = {
                "id": post.id,
                "title": post.title,
                "author": post.author,
                "intro": post.intro,
                "content": post.content,
                "format": post.format,
                "source": post.source,
                "original_url": post.original_url,
                "create_time": str(post.create_time.date()),
            }
        else:
            result = {}

        return result

    def get_all_posts(self, offset, limit, search=None):
        """get all posts
        :param offset: offset
        :param limit: limit
        :param search: search
        """
        query = self.db_session.query(PostModel)
        if search:
            offset = 0
            query = query.filter(or_(PostModel.title.contains(search),
                                     PostModel.intro.contains(search),
                                     PostModel.content.contains(search)))
        posts = self.fetch_all(query, offset=offset, limit=limit)
        if posts:
            result = [{
                "id": post.id,
                "title": post.title,
                "author": post.author,
                "intro": post.intro,
                "content": post.content,
                "format": post.format,
                "source": post.source,
                "original_url": post.original_url,
                "create_time": str(post.create_time.date()),
            } for post in posts]
        else:
            result = []

        return result

    def get_all_crawler_original_urls(self):
        """get all crawler origin urls"""
        query = self.db_session.query(PostModel.original_url)
        posts = self.fetch_all(query)
        if posts:
            result = [url for url, in posts]
        else:
            result = []

        return result


post_db = PostDB()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
