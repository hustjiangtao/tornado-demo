# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""all models of this project"""


from app.lib.utils import do_logging

from app.database.models.base_model import BaseModel
from app.database.models.base_model import engine

from app.database.models.demo import Demo as DemoModel
from app.database.models.user import User as UserModel
from app.database.models.post import Post as PostModel
from app.database.models.upload import Upload as UploadModel
from app.database.models.bookmark import Bookmark as BookmarkModel

__all__ = (
    'DemoModel',
    'UserModel',
    'PostModel',
    'UploadModel',
    'BookmarkModel',
)


if __name__ == '__main__':
    do_logging('create db start.')
    # BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
    do_logging('create db complete.')
