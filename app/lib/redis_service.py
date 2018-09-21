# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Redis service"""


import redis


pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r_cache = redis.Redis(connection_pool=pool)
