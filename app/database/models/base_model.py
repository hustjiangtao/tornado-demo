# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Base model settings"""


import json
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy import func

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.sql.expression import text


class DateTimeEncoder(json.JSONEncoder):
    """DateTime encoder"""

    def default(self, o):
        if isinstance(o, datetime):
            encoded_object = datetime.strftime(o, "%Y-%m-%dT%H:%M:%SGMT+08:00")
        else:
            encoded_object = json.JSONEncoder.default(self, o)
        return encoded_object


class MetaModel:
    """Base meta setting for sql obj"""

    id = Column(Integer, primary_key=True, autoincrement=True, comment='记录ID')
    create_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建时间')
    update_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    # create_time = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP()'), comment='创建时间')
    # create_time = Column(TIMESTAMP, server_default=text("(datetime('now','localtime'))"),
    #                      comment='创建时间')
    # update_time = Column(TIMESTAMP, nullable=False,
    #                      server_default=text('CURRENT_TIMESTAMP() on update CURRENT_TIMESTAMP()'),
    #                      comment='更新时间')

    @declared_attr
    def __tablename__(cls):
        """define table name, lower case with _ to split"""
        name = ''.join([f'_{x}' if x.isupper() and idx != 0 else x for idx, x in enumerate(cls.__name__)])
        return name.lower()

    @declared_attr
    def __table_args__(cls):
        return {'mysql_charset': 'utf8mb4', 'mysql_engine': 'InnoDB'}

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def to_dict(self, include=None):
        """transform sql obj to dict
        :param include: (list, tuple), item to return, eg: include=['id', 'name']
        """
        if include and isinstance(include, (list, tuple)):
            result = {x: getattr(self, x) for x in include}
        else:
            result = self.columnitems
        return result

    def to_json(self):
        """transform sql obj to json"""
        return json.dumps(self.to_dict(), cls=DateTimeEncoder)


class Engine:
    from config import SQL

    sql = SQL.get('db')
    engine = create_engine(f'{sql}', encoding='utf8', echo=False)


BaseModel = declarative_base(cls=MetaModel)
engine = Engine().engine
# Session = sessionmaker(bind=engine)
Session = scoped_session(sessionmaker(bind=engine))
