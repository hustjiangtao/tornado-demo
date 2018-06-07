# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado import gen

from database.models.post import Post


@gen.coroutine
def get_all_posts():
    post_service = Post()
    result = post_service.get_all_posts()
    raise gen.Return(result)


@gen.coroutine
def get_post_by_id(_id):
    post_service = Post()
    result = post_service.get_post_by_id(_id=_id)
    raise gen.Return(result)
