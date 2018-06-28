# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""
-- drop table if exists post;
create table if not exists post (
id INTEGER primary key AUTOINCREMENT ,
title varchar(100) not null ,
content text ,
author varchar(50) not null ,
create_time timestamp default (datetime('now', 'localtime')) ) ;
"""


from sqlalchemy import Column

from sqlalchemy.sql.sqltypes import TEXT
from sqlalchemy.sql.sqltypes import VARCHAR

from database.models.base_model import BaseModel


class Post(BaseModel):

    """post model"""

    title = Column(VARCHAR(100), nullable=False, comment='标题')
    content = Column(TEXT, comment='正文')
    author = Column(VARCHAR(50), comment='作者')
