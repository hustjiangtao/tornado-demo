# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import options

from settings import settings
from urls import url_handlers as handlers


class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    logging.info('Tornado server start...')
    main()
