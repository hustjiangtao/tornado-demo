# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""sql model route"""


import sys
sys.path.append('../../')

from lib.utils import do_logging

from database.models.base_model import BaseModel
from database.models.base_model import engine

from database.models.demo import Demo
from database.models.user import User
from database.models.post import Post
from database.models.upload import Upload


class Model:

    """all models of this project"""

    DemoModel = Demo
    UserModel = User
    PostModel = Post
    UploadModel = Upload


model = Model()
DemoModel = model.DemoModel
UserModel = model.UserModel
PostModel = model.PostModel
UploadModel = model.UploadModel


if __name__ == '__main__':
    do_logging('create db start.')
    # BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
    do_logging('create db complete.')
