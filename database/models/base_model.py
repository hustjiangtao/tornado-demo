# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import logging

from pymongo import MongoClient
from bson.objectid import ObjectId


class BaseModel(object):
    """Base model
    All other model should base on this BaseModel.
    """
    client = None
    db_name = 'test'

    def __init__(self, collection_name):
        self.db = self.__get_db(self.db_name, collection_name)

    @staticmethod
    def __get_client():
        """
        获取client
        :return:
        """
        try:
            client = MongoClient()
        except Exception as e:
            client = None
            logging.warning("mongodb connect error: {error}".format(error=e))

        return client

    def __get_db(self, db_name, collection_name):
        """
        获取db
        :param db_name:
        :param collection_name:
        :return:
        """
        if self.client is None:
            self.client = self.__get_client()
        db = self.client[db_name][collection_name]

        return db

    def fetch_one(self, _id=None, **kwargs):
        if _id:
            kwargs["_id"] = ObjectId(_id)
        return self.db.find_one(kwargs)

    def fetch_all(self, **kwargs):
        return self.db.find(kwargs)

    def add_item(self, item):
        return self.db.insert_one(item)

    def add_items(self, items):
        return self.db.insert_many(items)

    def update(self, item, _id=None, **kwargs):
        if _id:
            kwargs["_id"] = ObjectId(_id)
        return self.db.find_one_and_update(filter=kwargs, update=item)
