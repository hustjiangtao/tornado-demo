# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from database.models.base_model import BaseModel


class User(BaseModel):
    """User model
    user_model_example = {
        "id": 1,
        "account": 'I am account',
        "name": 'I am name',
        "email": 'jiangtao.work@gmail.com',
    }
    """

    def __init__(self):
        super(User, self).__init__(collection_name='user')

    def get_all_users(self):
        """Fetch all users"""
        result = self.fetch_all()
        if result:
            result = [{
                "id": int(x.get('id')),
                "name": x.get('name'),
            } for x in result]

        return result

    def get_user_by_name(self, name):
        """Fetch a user by his name"""
        result = self.fetch_one(name=name)
        if result:
            result = {
                "id": int(result.get('id')),
                "account": result.get('account'),
                "name": result.get('name'),
                "email": result.get('email'),
            }

        return result

    def add_user(self, name):
        """Add a user"""
        item = {
            "id": id,
            "name": name,
        }
        result = self.add_item(item=item)

        return result
