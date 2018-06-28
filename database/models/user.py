# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""
-- drop table if exists user;
create table if not exists user (
id INTEGER primary key AUTOINCREMENT ,
name varchar(50) not null unique ,
email varchar(50) not null unique ,
mobile varchar(20) ,
password char(64) not null ,
salt char(10) not null ,
create_time timestamp default (datetime('now', 'localtime')) ) ;
"""


from sqlalchemy import Column

from sqlalchemy.sql.sqltypes import CHAR
from sqlalchemy.sql.sqltypes import VARCHAR

from database.models.base_model import BaseModel


class User(BaseModel):

    """user model"""

    name = Column(VARCHAR(50), nullable=False, unique=True, comment='姓名')
    email = Column(VARCHAR(50), nullable=False, unique=True, comment='邮箱')
    mobile = Column(VARCHAR(20), comment='邮箱')
    password = Column(CHAR(64), nullable=False, comment='密码')
    salt = Column(CHAR(10), nullable=False, comment='salt')
