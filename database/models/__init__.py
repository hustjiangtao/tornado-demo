# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""all models of this project"""


from lib.utils import do_logging

from database.models.base_model import BaseModel
from database.models.base_model import engine

from database.models.demo import Demo as DemoModel
from database.models.user import User as UserModel
from database.models.post import Post as PostModel
from database.models.upload import Upload as UploadModel

__all__ = (
    'DemoModel',
    'UserModel',
    'PostModel',
    'UploadModel',
)


if __name__ == '__main__':
    do_logging('create db start.')
    # BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
    do_logging('create db complete.')
