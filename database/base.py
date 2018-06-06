# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import logging
import sqlite3


class BaseDB(object):
    """SQL
    All other sql class should base on this one
    """

    conn = sqlite3.connect('/Users/jiangtao.work/Desktop/test.db')

    def __init__(self):
        self.db = self.conn.cursor()

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
        finally:
            self.conn.close()

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
        finally:
            self.conn.close()

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
        finally:
            self.conn.close()

        return result

    def fetch_one(self, query):
        if not query:
            return None

        try:
            self.db.execute(query)
            result = self.db.fetchall()
        except Exception as e:
            logging.info(e)
            self.conn.rollback()
            result = []
        finally:
            self.conn.close()

        return result

    def add_item(self, insert_sql, params):
        if not insert_sql:
            return None

        try:
            self.db.execute(insert_sql, params)
            self.conn.commit()
            result = True
        except Exception as e:
            logging.info(e)
            self.conn.rollback()
            result = False
        finally:
            self.conn.close()

        return result
