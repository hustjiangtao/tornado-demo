# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""
-- drop table if exists demo;
create table if not exists demo (
id INTEGER primary key AUTOINCREMENT ,
name varchar(100) not null ,
new_name varchar(100) default null ,
size INTEGER not null ,
content_type varchar(10) not null ,
url varchar(120) not null ,
create_time timestamp default (datetime('now', 'localtime')) ) ;
"""


from sqlalchemy import Column

from sqlalchemy.sql.sqltypes import VARCHAR
from sqlalchemy.sql.sqltypes import Integer

from database.models.base_model import BaseModel


class Upload(BaseModel):

    """upload model"""

    name = Column(VARCHAR(100), nullable=False, comment='原始名称')
    new_name = Column(VARCHAR(100), comment='自定义名称')
    size = Column(Integer, nullable=False, comment='大小')
    content_type = Column(VARCHAR(10), nullable=False, comment='文件类型')
    url = Column(VARCHAR(120), nullable=False, unique=True, comment='链接')
