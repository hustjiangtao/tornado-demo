# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import datetime

from tornado.websocket import WebSocketHandler

from handlers.base_handler import BaseHandler


class ChatIndexHandler(BaseHandler):
    def get(self):
        self.render("functools/chat.html")


class ChatHandler(WebSocketHandler):

    users = set()  # 用来存放在线用户的容器

    def open(self):
        self.users.add(self)  # 建立连接后添加用户到容器中
        for u in self.users:  # 向已在线用户发送消息
            # u.write_message(u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            u.write_message("[%s]-[%s]-In" % (self.request.remote_ip, datetime.datetime.now().strftime("%H:%M:%S")))

    def on_message(self, message):
        for u in self.users:  # 向在线用户广播消息
            # u.write_message(u"[%s]-[%s]-说：%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))
            u.write_message("[%s]-[%s]-Said：\n%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

    def on_close(self):
        self.users.remove(self) # 用户关闭连接后从容器中移除用户
        for u in self.users:
            # u.write_message(u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            u.write_message("[%s]-[%s]-Out" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求
