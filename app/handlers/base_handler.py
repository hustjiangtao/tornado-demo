# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Base handler for requests handlers"""


import json
import functools
import urllib.parse as urlparse
from urllib.parse import urlencode

import tornado.web
from tornado.escape import to_unicode
from tornado.web import HTTPError
from tornado.web import MissingArgumentError

from app.lib.utils import json_decode
from app.lib.utils import random_string
from app.lib.utils import get_hashed_password
from app.lib.utils import compare_digest
from app.lib.system_code import ERROR
from app.lib.system_code import MESSAGE
from app.lib.redis_service import r_cache


def authenticated(method):
    """Decorate methods with this to require that the user be logged in.
    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.
    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


def api_authenticated(method):
    """Decorate methods with this to require that the user be logged in.
    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.
    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


class BaseHandler(tornado.web.RequestHandler):
    """Base class for other request handlers - all other handlers should
    base on this one.
    """
    r = r_cache
    r_cache = r_cache

    def initialize(self):
        self.__set_header()

    def __set_header(self):
        self.set_header("Server", "DemoServer")
        self.set_header("Cache-Control", "private")
        self.set_header('Version', 'v0.1')
        # self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.set_header('Content-Type', 'text/html; charset="utf-8"')
        self.set_header('Access-Control-Allow-Methods', 'POST, PUT, GET, OPTIONS, DELETE')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header(
            'Access-Control-Allow-Headers',
            'Origin, X-Requested-With, Content-Type, Accept, client_id, uuid, Authorization'
        )

        # # TODO test-only
        # self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin') or '*')

    def render_json(self, code=0, data=None, message=''):
        """
        return json formatted data
        :param code: int
        :param data: dict
        :param message: str
        :return: bool
        """
        if message == '':
            message = MESSAGE.get(code, ERROR)
        result = {
            "code": code,
            "message": message,
            "data": data,
        }
        self.write(json.dumps(result, ensure_ascii=False))

    def render(self, template_name, **kwargs):
        """
        Renders the template with the given arguments as the response.
        do not calls ``finish()``
        """
        from tornado.escape import utf8
        from tornado.util import unicode_type
        if self._finished:
            raise RuntimeError("Cannot render() after finish()")
        html = self.render_string(template_name, **kwargs)

        # Insert the additional JS and CSS added by the modules on the page
        js_embed = []
        js_files = []
        css_embed = []
        css_files = []
        html_heads = []
        html_bodies = []
        for module in getattr(self, "_active_modules", {}).values():
            embed_part = module.embedded_javascript()
            if embed_part:
                js_embed.append(utf8(embed_part))
            file_part = module.javascript_files()
            if file_part:
                if isinstance(file_part, (unicode_type, bytes)):
                    js_files.append(file_part)
                else:
                    js_files.extend(file_part)
            embed_part = module.embedded_css()
            if embed_part:
                css_embed.append(utf8(embed_part))
            file_part = module.css_files()
            if file_part:
                if isinstance(file_part, (unicode_type, bytes)):
                    css_files.append(file_part)
                else:
                    css_files.extend(file_part)
            head_part = module.html_head()
            if head_part:
                html_heads.append(utf8(head_part))
            body_part = module.html_body()
            if body_part:
                html_bodies.append(utf8(body_part))

        if js_files:
            # Maintain order of JavaScript files given by modules
            js = self.render_linked_js(js_files)
            sloc = html.rindex(b'</body>')
            html = html[:sloc] + utf8(js) + b'\n' + html[sloc:]
        if js_embed:
            js = self.render_embed_js(js_embed)
            sloc = html.rindex(b'</body>')
            html = html[:sloc] + js + b'\n' + html[sloc:]
        if css_files:
            css = self.render_linked_css(css_files)
            hloc = html.index(b'</head>')
            html = html[:hloc] + utf8(css) + b'\n' + html[hloc:]
        if css_embed:
            css = self.render_embed_css(css_embed)
            hloc = html.index(b'</head>')
            html = html[:hloc] + css + b'\n' + html[hloc:]
        if html_heads:
            hloc = html.index(b'</head>')
            html = html[:hloc] + b''.join(html_heads) + b'\n' + html[hloc:]
        if html_bodies:
            hloc = html.index(b'</body>')
            html = html[:hloc] + b''.join(html_bodies) + b'\n' + html[hloc:]
        return self.write(html)

    def check_xsrf_cookie(self):
        """Ignore xsrf if ajax"""
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return

    def data_received(self, chunk):
        """Implement this method for tornado.web.RequestHandler"""
        pass

    def get_current_user(self):
        """determine the current user from, e.g., a cookie."""
        user_cookie = self.get_secure_cookie("user")
        if user_cookie:
            return json.loads(user_cookie)
        return None

    # default args for json_arguments, default is object, not none
    _ARG_DEFAULT=object()

    def get_json_argument(self, name, default=_ARG_DEFAULT):
        """Get argument from application/json body"""
        content_type = self.request.headers.get("Content-Type", "")
        if content_type.startswith("application/json"):
            args = json_decode(self.request.body)
            name = to_unicode(name)
            if name in args:
                result = args[name]
            elif default is self._ARG_DEFAULT:
                raise MissingArgumentError(name)
            else:
                result = default

            return result

        return None

    @staticmethod
    def get_new_password(password):
        """Generate a password"""
        salt = random_string(10)
        hashed_password = get_hashed_password(password=password, salt=salt)
        return hashed_password, salt

    @staticmethod
    def is_my_password(new_password, my_password, my_salt):
        """Compare if a given password is my password"""
        hashed_password = get_hashed_password(password=new_password, salt=my_salt)
        return compare_digest(hashed_password, my_password)
