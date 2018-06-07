# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from database.models.base_model import BaseModel


class Post(BaseModel):
    """Post model
    post_model_example = {
        "id": 1,
        "title": 'I am title',
        "content": 'I am content',
        "tag": 'post,user',
    }
    """
    {"id": 1,"title": 'I am title',"content": 'I am content',"tag": 'post,user'}

    def __init__(self):
        super(Post, self).__init__(collection_name='post')

    def get_all_posts(self):
        """Fetch all posts"""
        result = self.fetch_all()
        if result:
            result = [{
                "id": int(x.get('id')),
                "title": x.get('title'),
                "content": x.get('content'),
                "tag": x.get('tag').split(',') if x.get('tag') else [],
            } for x in result]

        return result

    def get_post_by_id(self, _id):
        """Fetch a user by it's id"""
        result = self.fetch_one(id=float(_id))
        if result:
            result = {
                "id": int(result.get('id')),
                "title": result.get('title'),
                "content": result.get('content'),
                "tag": result.get('tag').split(',') if result.get('tag') else [],
            }

        return result

    def add_post(self, title, content, tag):
        """Add a post"""
        item = {
            "id": 1,
            "title": title,
            "content": content,
            "tag": tag,
        }
        result = self.add_item(item=item)

        return result

    def update_post(self, _id, title, content, tag):
        """Update a post"""
        item = {
            "id": _id,
            "title": title,
            "content": content,
            "tag": tag,
        }
        result = self.update(item=item, _id=_id)

        return result
