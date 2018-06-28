# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from database.base import BaseDB
from database.models.model_route import PostModel


class PostDB(BaseDB):
    """Post DB"""

    def add_post(self, item):
        """Add a post
        >>> {"title": 'jiangtao-first-post', "content": 'my email is jiangtao.hu@qq.com', "author": 'jiangtao'}
        True
        """
        if not isinstance(item, dict):
            return False

        post_model = PostModel()
        post_model.title = item.get('title')
        post_model.content = item.get('content')
        post_model.author = item.get('author')

        result = self.add(post_model)
        if result:
            result = post_model.id

        return result

    def add_crawler_posts(self, items):
        """Add a post
        >>> [{"title": 'jiangtao-first-post', "content": 'my email is jiangtao.hu@qq.com', "author": 'jiangtao'}]
        True
        """
        if not isinstance(items, list):
            return False

        post_models = []
        for item in items:
            post_model = PostModel()
            post_model.title = item.get('title')
            post_model.intro = item.get('content')
            post_model.content = item.get('content')
            post_model.author = item.get('author')
            post_model.source = item.get('source')
            post_model.source_id = item.get('source_id')
            post_model.original_url = item.get('original_url')
            post_model.collection_count = item.get('collection_count')
            post_model.comments_count = item.get('comments_count')
            if item.get('create_time'):
                post_model.create_time = item.get('create_time')

            post_models.append(post_model)

        result = self.add_all(post_models)
        if result:
            result = True

        return result

    def update_post(self, _id, item):
        """update a post
        >>> {"title": 'jiangtao-first-post', "content": 'my email is jiangtao.hu@qq.com'}
        True
        """
        if not _id or not isinstance(item, dict):
            return False

        query = self.db_session.query(PostModel).filter_by(id=_id)
        post = self.fetch_first(query)
        if not post:
            return False

        post.title = item.get('title')
        post.content = item.get('content')
        result = self.save(post)

        return result

    def get_post_by_id(self, _id):
        """get a post by it's id
        >>> 1
        True
        """
        if not _id:
            return {}

        query = self.db_session.query(PostModel).filter_by(id=_id)
        post = self.fetch_first(query)
        if post:
            result = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author": post.author,
                "create_time": post.create_time,
            }
        else:
            result = {}

        return result

    def get_all_posts(self):
        """get all posts
        >>>
        True
        """
        query = self.db_session.query(PostModel)
        posts = self.fetch_all(query)
        if posts:
            result = [{
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author": post.author,
                "create_time": post.create_time,
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
    post_db = PostDB()
    print(post_db.add_post({
        "title": 'jiangtao-first-post',
        "content": 'my email is jiangtao.hu@qq.com',
        "author": 'jiangtao'
    }))
