# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Base db operations"""


import logging
import traceback

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import NoResultFound

from database.models.base_model import Session


class BaseDB:
    """SQL
    All other sql class should base on this one
    """

    def __init__(self):
        self.db_session = Session()

    def __del__(self):
        self.db_session.close()

    def add(self, instance):
        """add a instance"""
        if not instance:
            return False

        try:
            self.db_session.add(instance)
            self.db_session.commit()
            result = True
        except OperationalError:
            self.db_session.rollback()
            logging.warning(traceback.format_exc())
            result = False

        return result

    def add_all(self, instances):
        """add many instances"""
        if not instances:
            return False

        try:
            self.db_session.add_all(instances)
            self.db_session.commit()
            result = True
        except OperationalError:
            self.db_session.rollback()
            logging.warning(traceback.format_exc())
            result = False

        return result

    def save(self, instance):
        """save instance while modified"""
        if not instance:
            return False

        try:
            self.db_session.commit()
            result = True
        except OperationalError:
            self.db_session.rollback()
            logging.warning(traceback.format_exc())
            result = False

        return result

    @staticmethod
    def fetch_first(query):
        """fetch first result after query"""
        if not query:
            return None

        try:
            result = query.first()
        except NoResultFound:
            logging.warning(traceback.format_exc())
            result = None

        return result

    @staticmethod
    def fetch_all(query, offset=None, limit=None):
        """fetch all result after query"""
        if not query:
            return None

        if offset is not None and limit is not None:
            query = query.offset(offset).limit(limit)

        try:
            result = query.all()
        except NoResultFound:
            logging.warning(traceback.format_exc())
            result = []

        return result

    @staticmethod
    def count(query):
        """fetch count after query"""
        if not query:
            return None

        try:
            result = query.first()
            if result:
                result = result[0]
        except NoResultFound:
            logging.warning(traceback.format_exc())
            result = None

        return result
