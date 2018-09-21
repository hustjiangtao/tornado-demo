# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""server for project"""


import logging
import traceback
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import options

from app.settings import SETTINGS
from app.urls import URL_HANDLERS


class Application(tornado.web.Application):
    """initial application"""

    def __init__(self):
        tornado.web.Application.__init__(self, URL_HANDLERS, **SETTINGS)


def main():
    """main function to run server"""
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    try:
        logging.warning('ICE server start...')
        main()
    except KeyboardInterrupt:
        logging.warning("KeyboardInterrupt")
    else:
        logging.warning(traceback.format_exc())
