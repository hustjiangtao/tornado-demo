# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

from sqlalchemy import Column

from sqlalchemy.sql.sqltypes import CHAR
from sqlalchemy.sql.sqltypes import VARCHAR

from app.database.models.base_model import BaseModel


class User(BaseModel):
    """user model"""
    name = Column(VARCHAR(50), nullable=False, unique=True, comment='姓名')
    email = Column(VARCHAR(50), nullable=False, unique=True, comment='邮箱')
    mobile = Column(VARCHAR(20), comment='邮箱')
    password = Column(CHAR(64), nullable=False, comment='密码')
    salt = Column(CHAR(10), nullable=False, comment='salt')


class Demo(BaseModel):
    """demo model"""
    name = Column(VARCHAR(50), nullable=False, unique=True, comment='姓名')
