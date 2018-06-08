# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import logging
import sqlite3


class RowObj(sqlite3.Row):
    """格式化sql返回数据为字典格式
    eg. (4, '111', 'aaa', 'jiangtao', '2018-06-08 09:42:52')
    -->
    RowObj({'id': 4, 'title': '111', 'content': 'aaa', 'author': 'jiangtao', 'create_time': '2018-06-08 09:42:52'})
    """

    def __repr__(self):
        return '{}({})'.format(
                self.__class__.__name__, {x: self[x] for x in self.keys()})


class BaseDB(object):
    """SQL
    All other sql class should base on this one
    """

    conn = sqlite3.connect('/Users/jiangtao.work/Desktop/test.db')
    conn.row_factory = RowObj

    def __init__(self):
        self.db = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def create_db(self, create_sql):
        if not create_sql:
            return False

        try:
            self.db.execute(create_sql)
            self.conn.commit()
            result = True
        except Exception as e:
            logging.info(e)
            self.conn.rollback()
            result = False

        return result

    def fetch_all(self, query):
        if not query:
            return None

        try:
            self.db.execute(query)
            result = self.db.fetchall()
        except Exception as e:
            logging.info(e)
            self.conn.rollback()
            result = []

        return result

    def fetch_many(self, query, size):
        if not all([query, size]):
            return None

        try:
            self.db.execute(query)
            result = self.db.fetchmany(size=size)
        except Exception as e:
            logging.info(e)
            self.conn.rollback()
            result = []

        return result

    def fetch_one(self, query):
        if not query:
            return None

        try:
            self.db.execute(query)
            result = self.db.fetchone()
        except Exception as e:
            logging.info(e)
            self.conn.rollback()
            result = None

        return result

    def add_item(self, insert_sql, params):
        if not insert_sql:
            return None

        try:
            self.db.execute(insert_sql, params)
            self.conn.commit()
            # return id if insert success else 0
            result = self.db.lastrowid
        except Exception as e:
            logging.info(e)
            self.conn.rollback()
            result = False

        return result

    def update_item(self, sql, params):
        if not sql:
            return None

        try:
            self.db.execute(sql, params)
            self.conn.commit()
            result = True
        except Exception as e:
            logging.info(e)
            self.conn.rollback()
            result = False

        return result
