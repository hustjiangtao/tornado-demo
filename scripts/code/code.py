# -*- coding: utf-8 -*-


from time import time, sleep
from random import shuffle
from functools import lru_cache


def q_s(l):
    if len(l) <= 1:
        return l
    else:
        a = l[0]
        # print(a)
        g_l = [x for x in l[1:] if x > a]
        l_l = [x for x in l[1:] if x <= a]
        return q_s(l_l) + [a] + q_s(g_l)


# t=time()
# a_list = list(range(1000))
# shuffle(a_list)
# # print(a_list)
# q_s(a_list)
# # print(q_s(a_list))
# # for x in r_s(a_list):
#     # print(x, end=', ')
#     # pass
# print(time()-t)
#
#
# t=time()
# a_list = list(range(10))
# shuffle(a_list)
# print(a_list)
# print(q_s(a_list))
# # for x in r_s(a_list):
#     # print(x, end=', ')
#     # pass
# # print('\n')
# print(time()-t)


@lru_cache(maxsize=1)
def maopao(n):
    l = [2, 3, 1, 7, 4]
    count = len(l)
    for ix in range(count):
        for iy in range(ix + 1, count):
            # print(l[ix], l[iy])
            # print(l)
            if l[ix] > l[iy]:
                l[ix], l[iy] = l[iy], l[ix]

    # print(l)
    # print(sleep(0.5))
    # print(n)
    return time()


# t_l = [2, 3, 1, 7, 4]
# maopao(t_l)
for x in range(12):
    # print(x%3)
    l = maopao(x%2)
    # print(l)
    # print(maopao.cache_info())


from functools import lru_cache


@lru_cache(maxsize=10)
def print_num(n):
    print(f'I can cache this num after first print {n}')


if __name__ == "__main__":
    for n in range(10):
        print_num(n%3)
        print(f'cached {n}')
