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
from sqlalchemy import text

from sqlalchemy.sql.sqltypes import TEXT
from sqlalchemy.sql.sqltypes import VARCHAR
from sqlalchemy.sql.sqltypes import Integer

from database.models.base_model import BaseModel


class Post(BaseModel):

    """post model"""

    title = Column(VARCHAR(100), nullable=False, comment='标题')
    intro = Column(TEXT, comment='简介')
    content = Column(TEXT, comment='正文')
    author = Column(VARCHAR(50), nullable=False, comment='作者')
    source = Column(VARCHAR(10), comment='来源')
    source_id = Column(VARCHAR(64), comment='来源站内id')
    original_url = Column(VARCHAR(128), comment='原始链接')
    collection_count = Column(Integer, nullable=False, server_default=text('0'), comment='收藏数')
    comments_count = Column(Integer, nullable=False, server_default=text('0'), comment='评论数')
