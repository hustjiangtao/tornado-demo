# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""doc model"""


from sqlalchemy import Column
from sqlalchemy import Integer

from sqlalchemy.sql.sqltypes import VARCHAR
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.dialects.mysql import TEXT

from sqlalchemy.sql.expression import text

from app.database.models.base_model import BaseModel


class Doc(BaseModel):

    """doc model"""

    title = Column(VARCHAR(50), nullable=False, server_default=text("''"), comment='标题')
    author = Column(Integer, nullable=False, server_default=text('0'), index=True, comment='作者id')
    category = Column(VARCHAR(50), nullable=False, server_default=text("''"), index=True, comment='分类')
    tag = Column(VARCHAR(50), nullable=False, server_default=text("''"), comment='标签')
    content = Column(TEXT, comment='正文')
    status = Column(TINYINT(4), nullable=False, server_default=text('0'), comment='状态')
    read_count = Column(Integer, nullable=False, server_default=text('0'), comment='阅读数')
