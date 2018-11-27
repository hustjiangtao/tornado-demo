# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""mv model"""

from datetime import date
from sqlalchemy import Column, ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql.sqltypes import VARCHAR, Integer, Date
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.hybrid import hybrid_property

from app.database.models.base_model import BaseModel


class Mv(BaseModel):

    """mv model"""

    name = Column(VARCHAR(100), nullable=False, server_default=text("''"), index=True, comment='名称')
    url = Column(VARCHAR(256), nullable=False, server_default=text("''"), index=True, comment='链接')
    ori_url = Column(VARCHAR(256), nullable=False, server_default=text("''"), comment='原始链接')
    download_url = Column(VARCHAR(256), nullable=False, server_default=text("''"), comment='下载链接')
    cover_url = Column(VARCHAR(256), nullable=False, server_default=text("''"), comment='封面链接')
    type = Column(VARCHAR(32), nullable=False, server_default=text("''"), comment='分类')
    info = Column(VARCHAR(100), nullable=False, server_default=text("''"), comment='介绍')
    creator = Column(Integer, nullable=False, server_default=text('0'), comment='创建者')
    source = Column(VARCHAR(256), nullable=False, server_default=text("''"), comment='来源')
    duration = Column(Integer, nullable=False, server_default=text('0'), comment='时长, 单位毫秒')
    size = Column(Integer, nullable=False, server_default=text('0'), comment='大小，单位字节')
    width = Column(Integer, nullable=False, server_default=text('0'), comment='宽度')
    height = Column(Integer, nullable=False, server_default=text('0'), comment='高度')
    stats = relationship("MvStats",
                         foreign_keys="MvStats.id",
                         backref="mv", lazy="dynamic")

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


class MvStats(BaseModel):

    """mv stats model"""

    id = Column(Integer, ForeignKey('mv.id'), primary_key=True, comment='mv ID')
    click = Column(Integer, nullable=False, server_default=text('0'), comment='点击')
    like = Column(Integer, nullable=False, server_default=text('0'), comment='喜欢')
    dislike = Column(Integer, nullable=False, server_default=text('0'), comment='不喜欢')

    @hybrid_property
    def rate(self):
        """评分/热度"""
        return self.click + 3 * self.like - 5 * self.dislike
