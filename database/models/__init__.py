# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""all models of this project"""


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
