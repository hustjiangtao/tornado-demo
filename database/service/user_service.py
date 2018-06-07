# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado import gen

from database.models.user import User


@gen.coroutine
def get_user_by_name(name):
    user_service = User()
    result = user_service.get_user_by_name(name=name)
    raise gen.Return(result)
