# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""url handlers for web server"""


from tornado.web import RedirectHandler

from app.handlers.test import TestHandler
from app.handlers.health import HealthHandler
from app.handlers.demo import demo
from app.handlers.auth import register
from app.handlers.auth import auth
from app.handlers.user import user
from app.handlers.post import post_list
from app.handlers.post import post
from app.handlers.tools import chat
from app.handlers.tools import upload
from app.handlers.album import album
from app.handlers.blog import blog
from app.handlers.blog import about
from app.handlers.blog import contact


URL_HANDLERS = []


__BASE_URL_HANDLERS = [
    (r"/", RedirectHandler, dict(url='/posts', permanent=False)),
    (r"/test", TestHandler),
    (r"/health", HealthHandler),
    (r"/demo", demo.DemoHandler),
    (r"/register", register.RegisterHandler),
    (r"/auth", auth.AuthHandler),
    (r"/user", user.UserHandler),
    (r"/posts", post_list.PostListHandler),
    (r"/post", post.PostHandler),
    (r"/chat-index", chat.ChatIndexHandler),
    (r"/chat", chat.ChatHandler),
    (r"/upload", upload.UploadHandler),
    (r"/album", album.AlbumHandler),
]


__MDL_BLOG_URL_HANDLERS = [
    (r"/index", post_list.PostListHandler),
    (r"/blog", blog.BlogHandler),
    (r"/about", about.AboutHandler),
    (r"/contact", contact.ContactHandler),
]


URL_HANDLERS.extend(__BASE_URL_HANDLERS)
URL_HANDLERS.extend(__MDL_BLOG_URL_HANDLERS)
