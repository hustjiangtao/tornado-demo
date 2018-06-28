# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import json

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.sql.expression import text


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            encoded_object = datetime.strftime(obj, "%Y-%m-%dT%H:%M:%SGMT+08:00")
        else:
            encoded_object = json.JSONEncoder.default(self, obj)
        return encoded_object


class MetaModel(object):

    id = Column(Integer, primary_key=True, autoincrement=True, comment='记录ID')
    # create_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP()'), comment='创建时间')
    create_time = Column(TIMESTAMP, server_default=text("(datetime('now','localtime'))"), comment='创建时间')
    # update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP() on update CURRENT_TIMESTAMP()'), comment='更新时间')
    # update_time = Column(TIMESTAMP, server_default=text("(datetime('now','localtime')) on update (datetime('now','localtime'))"), server_onupdate=text("(datetime('now','localtime'))"), comment='更新时间')

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def __table_args__(cls):
        return {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def to_dict(self):
        return self.columnitems

    def to_json(self):
        return json.dumps(self.to_dict(), cls=DateTimeEncoder)


class Engine(object):
    path = '/Users/jiangtao.work/Desktop/test.db'
    engine = create_engine('sqlite:///{path}'.format(path=path, encoding='utf8', echo=False))


BaseModel = declarative_base(cls=MetaModel)
engine = Engine().engine
Session = sessionmaker(bind=engine)
