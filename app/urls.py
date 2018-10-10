# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""url handlers for web server"""


from tornado.web import RedirectHandler
from tornado.web import url
from tornado.web import StaticFileHandler

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
from app.handlers.bookmark import bookmark_index
from app.handlers.bookmark import bookmark_view
from app.handlers.bookmark import bookmark_detail
from app.handlers.bookmark import bookmark_stats
from app.handlers.mm import mm_explore
from app.handlers.mm import mm_stats

from app.settings import SETTINGS


URL_HANDLERS = []


__BASE_URL_HANDLERS = [
    (r"/", RedirectHandler, dict(url='/bookmark/index', permanent=False)),
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


__BSP_URL_HANDLERS = [
    url(r"/bookmark/index", bookmark_index.IndexHandler, name="bookmark_index"),
    url(r"/bookmark/view", bookmark_view.ViewHandler, name="bookmark_view"),
    url(r"/bookmark", bookmark_detail.BookmarkDetailHandler, name="bookmark_detail"),
]


__BSP_STATS_API_HANDLERS = [
    url(r"/bookmark/stats/click", bookmark_stats.ClickHandler, name="bookmark_stats_click"),
    url(r"/mm/stats/click", mm_stats.ClickHandler, name="mm_stats_click"),
]


__MM_URL_HANDLERS = [
    url(r"/mm/explore", mm_explore.ExploreHandler, name="mm_explore"),
    # url(r"/mm/(.*\.(jpg|png|gif))", StaticFileHandler, dict(path=SETTINGS['ext_static_path']), name='mm_url'),
    url(r"/mm/(.*)", StaticFileHandler, dict(path=SETTINGS['ext_static_path']), name='mm_url'),
]


URL_HANDLERS.extend(__BASE_URL_HANDLERS)
URL_HANDLERS.extend(__MDL_BLOG_URL_HANDLERS)
URL_HANDLERS.extend(__BSP_URL_HANDLERS)
URL_HANDLERS.extend(__BSP_STATS_API_HANDLERS)
URL_HANDLERS.extend(__MM_URL_HANDLERS)
