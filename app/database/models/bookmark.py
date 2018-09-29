# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""bookmark model"""

from datetime import date
from sqlalchemy import Column, ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql.sqltypes import VARCHAR, Integer, Date
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.hybrid import hybrid_property

from app.database.models.base_model import BaseModel


class Bookmark(BaseModel):

    """bookmark model"""

    name = Column(VARCHAR(100), nullable=False, index=True, comment='名称')
    url = Column(VARCHAR(256), nullable=False, index=True, comment='链接')
    type = Column(VARCHAR(32), nullable=False, comment='分类')
    info = Column(VARCHAR(100), nullable=False, server_default=text("''"), comment='介绍')
    creator = Column(Integer, nullable=False, index=True, comment='创建者')
    stats = relationship("BookmarkStats",
                         foreign_keys="BookmarkStats.id",
                         backref="bookmark", lazy="dynamic")

    @hybrid_property
    def sum_stats(self, _type=None):
        """sum stats, eg: sum click, sum rate, return all stats when _type is None"""
        all_type = ('click', 'like', 'dislike', 'rate')

        if _type is None:
            all_stats = [{t: getattr(x, t) for t in all_type} for x in self.stats.all()]
            sum_stats = {t: sum([x.get(t) for x in all_stats]) for t in all_type}
        elif _type in all_type:
            sum_stats = sum([getattr(x, _type) for x in self.stats.all()])
        else:
            sum_stats = 0

        return sum_stats


class BookmarkStats(BaseModel):

    """bookmark stats model"""

    id = Column(Integer, ForeignKey('bookmark.id'), primary_key=True, comment='bookmark ID')
    click = Column(Integer, nullable=False, server_default=text('0'), comment='点击')
    like = Column(Integer, nullable=False, server_default=text('0'), comment='喜欢')
    dislike = Column(Integer, nullable=False, server_default=text('0'), comment='不喜欢')

    @hybrid_property
    def rate(self):
        """评分/热度"""
        return self.click + 3 * self.like - 5 * self.dislike
