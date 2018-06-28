# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import logging
import traceback

from database.models.base_model import Session


class BaseDB(object):
    """SQL
    All other sql class should base on this one
    """

    def __init__(self):
        self.db_session = Session()

    def __del__(self):
        self.db_session.close()

    def add(self, instance):
        if not instance:
            return False

        try:
            self.db_session.add(instance)
            self.db_session.commit()
            result = True
        except Exception as e:
            self.db_session.rollback()
            logging.warning(traceback.format_exc())
            result = False

        return result

    def add_all(self, instances):
        if not instances:
            return False

        try:
            self.db_session.add_all(instances)
            self.db_session.commit()
            result = True
        except Exception as e:
            self.db_session.rollback()
            logging.warning(traceback.format_exc())
            result = False

        return result

    def save(self, instances):
        if not instances:
            return False

        try:
            self.db_session.commit()
            result = True
        except Exception as e:
            self.db_session.rollback()
            logging.warning(traceback.format_exc())
            result = False

        return result

    @staticmethod
    def fetch_first(query):
        if not query:
            return None

        try:
            result = query.first()
        except Exception as e:
            logging.warning(traceback.format_exc())
            result = None

        return result

    @staticmethod
    def fetch_all(query, offset=None, limit=None):
        if not query:
            return None

        if offset is not None and limit is not None:
            query = query.offset(offset).limit(limit)

        try:
            result = query.all()
        except Exception as e:
            logging.warning(traceback.format_exc())
            result = []

        return result

    @staticmethod
    def count(query):
        if not query:
            return None

        try:
            result = query.first()
            if result:
                result = result[0]
        except Exception as e:
            logging.warning(traceback.format_exc())
            result = None

        return result
