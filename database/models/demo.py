# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""
-- drop table if exists demo;
create table if not exists demo (
id INTEGER primary key AUTOINCREMENT ,
name varchar(50) not null unique ,
create_time timestamp default (datetime('now', 'localtime')) ) ;
"""


from sqlalchemy import Column

from sqlalchemy.sql.sqltypes import VARCHAR

from database.models.base_model import BaseModel


class Demo(BaseModel):

    """demo model"""

    name = Column(VARCHAR(50), nullable=False, unique=True, comment='姓名')
