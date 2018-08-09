# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""
-- drop table if exists post;
create table if not exists post (
id INTEGER primary key AUTOINCREMENT ,
title varchar(100) not null ,
author varchar(50) not null ,
tag varchar(32) ,
intro varchar(300) ,
content text ,
format varchar(10) ,
source varchar(10) ,
source_id varchar(64) ,
original_url varchar(128) ,
original_url timestamp default (datetime('now', 'localtime')) ) ;
"""


from sqlalchemy import Column

from sqlalchemy.sql.sqltypes import TEXT
from sqlalchemy.sql.sqltypes import VARCHAR

from database.models.base_model import BaseModel


class Post(BaseModel):

    """post model"""

    title = Column(VARCHAR(100), nullable=False, comment='标题')
    author = Column(VARCHAR(50), nullable=False, comment='作者')
    tag = Column(VARCHAR(32), comment='标签')
    intro = Column(VARCHAR(300), comment='简介')
    content = Column(TEXT, comment='正文')
    format = Column(VARCHAR(10), comment='格式')
    source = Column(VARCHAR(10), comment='来源')
    source_id = Column(VARCHAR(64), comment='来源站内id')
    original_url = Column(VARCHAR(128), comment='原始链接')
