# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import sys
sys.path.append('../../')

from lib.utils import do_logging

from database.models.base_model import BaseModel
from database.models.base_model import engine

from database.models.user import User
from database.models.post import Post
from database.models.demo import Demo


class Model(object):

    """all models of this project"""

    UserModel = User
    PostModel = Post
    DemoModel = Demo


model = Model()
UserModel = model.UserModel
PostModel = model.PostModel
DemoModel = model.DemoModel


if __name__ == '__main__':
    do_logging('create db start.')
    # BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
    do_logging('create db complete.')
