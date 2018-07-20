# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Chat"""


import datetime

from tornado.websocket import WebSocketHandler

from handlers.base_handler import BaseHandler


class ChatIndexHandler(BaseHandler):
    """Chat index page"""

    def get(self):
        self.render("functools/chat.html")


class ChatHandler(WebSocketHandler):
    """Chat handler"""

    def data_received(self, chunk):
        """Implement this method to handle streamed request data.

        Requires the `.stream_request_body` decorator.
        """
        raise NotImplementedError()

    users = set()  # 用来存放在线用户的容器

    def open(self):
        self.users.add(self)  # 建立连接后添加用户到容器中
        for user in self.users:  # 向已在线用户发送消息
            # user.write_message(u"[%s]-[%s]-进入聊天室" % (
            #     self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            user.write_message("[%s]-[%s]-In" % (
                self.request.remote_ip, datetime.datetime.now().strftime("%H:%M:%S")))

    def on_message(self, message):
        for user in self.users:  # 向在线用户广播消息
            # user.write_message(u"[%s]-[%s]-说：%s" % (
            #     self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #     message))
            user.write_message("[%s]-[%s]-Said：\n%s" % (
                self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                message))

    def on_close(self):
        self.users.remove(self) # 用户关闭连接后从容器中移除用户
        for user in self.users:
            # user.write_message(u"[%s]-[%s]-离开聊天室" % (
            #     self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            user.write_message("[%s]-[%s]-Out" % (
                self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求
