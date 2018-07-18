# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import time
import logging

from tornado import ioloop


class TimerTask(object):
    def __init__(self):
        def _test_task():
            logging.info('task complete.')
            # print(123333)
        print('start.')
        self._timer_task = ioloop.PeriodicCallback(
            _test_task,
            # 20*1000)
            2*1000)

    def start(self):
        self._timer_task.start()

    def stop(self):
        self._timer_task.stop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    t = TimerTask()
    t.start()
    # t.stop()
    ioloop.IOLoop.instance().start()