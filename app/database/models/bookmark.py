# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""bookmark model"""


from sqlalchemy import Column

from sqlalchemy.sql.sqltypes import VARCHAR, Integer
from sqlalchemy.sql.expression import text

from app.database.models.base_model import BaseModel


class Bookmark(BaseModel):

    """bookmark model"""

    name = Column(VARCHAR(100), nullable=False, index=True, comment='名称')
    url = Column(VARCHAR(256), nullable=False, index=True, comment='链接')
    type = Column(VARCHAR(32), nullable=False, comment='分类')
    info = Column(VARCHAR(100), nullable=False, server_default=text("''"), comment='介绍')
    creator = Column(Integer, nullable=False, index=True, comment='创建者')
