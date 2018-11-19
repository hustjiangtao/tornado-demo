# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""weibo handler"""


import os
import logging
import requests
import traceback
import json
import time
import re
import looter as lt
import urllib.parse
import urllib.request as urllib2

from datetime import date

from app.lib.mail import send_msg_by_email
from app.scripts.convert_md import convert_md, convert_full_html


domain = 'https://s.weibo.com'
base_top_url = f'{domain}/top/summary?cate='
realtimehot = f'{base_top_url}realtimehot'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': f'{domain}'  # 必须设定referer，否则会被重定向
}


def crawl(url):
    tree = lt.fetch(url)
    news_list = tree.css('#pl_top_realtimehot > table > tbody > tr')
    result = []
    for news in news_list[:20]:
        news_id = news.css('td.td-01.ranktop::text').extract_first()
        if not news_id:
            continue
        news_url = news.css('td.td-02 > a::attr(href)').extract_first()
        # sometimes url set in href_to instead of href
        if news.css('td.td-02 > a::attr(href_to)').extract_first():
            news_url = news.css('td.td-02 > a::attr(href_to)').extract_first()
        news_content = news.css('td.td-02 > a::text').extract_first()
        news_count = news.css('td.td-02 > span::text').extract_first()
        # get first detail of this news
        detail_tree = lt.fetch(domain+news_url, headers=headers)
        # detail = detail_tree.css('#pl_feedlist_index > div > div[action-type=feed_list_item]:nth-child(1) [node-type=feed_list_content] ::text').extract()
        detail = None
        n = 1
        while not detail:
            detail = detail_tree.css(f'#pl_feedlist_index > div > div[action-type=feed_list_item]:nth-child({n}) [node-type=feed_list_content] ::text').extract()
            n += 1
        news_detail = ''.join(detail).strip() if detail else ''
        # print(news_id, news_url, news_content, news_count, news_detail)
        result.append((news_id, domain+news_url, news_content, news_count, news_detail))

    return result


def word_filter(data):
    """filter word"""
    if not data:
        return ''

    words = ['#']
    for w in words:
        data = data.replace(w, f'\\{w}')

    return data


def format_to_md(data):
    """format to html"""
    if not data:
        return None
    head = f'## 微博实时热搜榜 {date.today()}\n\n'
    items = '<hr>\n\n'.join([f'- {id} {count} [{word_filter(content)}]({url}) \n\n\t{word_filter(detail)}\n' for id, url, content, count, detail in data])
    foot = '\n'
    module = head + items + foot
    # with open('weibo.md', 'wb') as f:
    #     f.write(bytes(module, encoding='utf-8'))
    module = ''.join(module)

    return module


def format_to_html(data):
    """format to html"""
    if not data:
        return None
    module = format_to_md(data)
    # module = convert_md(module)
    module = convert_full_html(module)

    return module


def convert_html_to_image(html):
    """convert html to image"""
    import imgkit
    options = {
        "encoding": 'UTF-8',
    }
    imgkit.from_string(html, 'out.jpg', options=options)


def convert_url_to_image(url):
    """convert html to image"""
    import imgkit
    options = {
        "encoding": 'UTF-8',
    }
    imgkit.from_url(url, 'ooo.jpg', options=options)


def send_msg(msg, attach_file=None):
    mail_to = 'hujiangtao@diyidan.com'
    to_name = 'jiangtao'
    subject = f'微博实时热搜榜 {date.today()}'
    return send_msg_by_email(mail_to=mail_to, msg=msg, to_name=to_name, subject=subject, attach_file=attach_file)


class Weibo:

    """weibo handler"""

    __WEIBO_CODE = {
        "100000": 'post_success',
    }
    __COOKIE_FILE = 'cookiejar.dat'

    def __init__(self):
        self.__uid = None
        self.__login()
        self.__opener = self.get_opener()
        self.send_http_request = self.__send_http_request
        pass

    def __check_cookiejar(self, cookie_file):
        """check if the cookiejar expired or not"""
        MAX_EPS=86400  # 24 hours
        if os.path.exists(cookie_file):
            modtime = os.stat(cookie_file).st_mtime
            if time.time() - modtime < MAX_EPS:
                return True

        return None

    def get_opener(self):
        """get urllib opener"""
        import http.cookiejar as cookielib

        cookie_file = self.__COOKIE_FILE
        cookie = cookielib.MozillaCookieJar()
        cookie.load(cookie_file, ignore_expires=True, ignore_discard=True)
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        opener.addheaders = [
            ("User-agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0'),
            # ("Referer", ("http://weibo.com/u/%s/home?wvr=" % self.__uid)),
            ("Referer", 'http://weibo.com'),
            ("Content-type", 'application/json')
        ]

        return opener

    @staticmethod
    def __build_url_request(url, data):
        return urllib2.Request(url, urllib.parse.urlencode(data).encode("utf-8"))

    def __send_http_request(self, url, data):
        req = self.__build_url_request(url, data)
        # print(req.get_full_url())
        try:
            resp = self.__opener.open(req)
            result = resp.read()
            # logging.info(result)
        except Exception as e:
            result = None
            logging.warning(traceback.format_exc())

        return result

    def __login(self):
        """登录，cookie有过期时间(1d)"""
        import rsa
        import binascii
        import base64
        import http.cookiejar as cookielib

        cookie_file = self.__COOKIE_FILE
        if self.__check_cookiejar(cookie_file):
            return

        def pre_login():
            pre_login_url='http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=MTUyNTUxMjY3OTY%3D&rsakt=mod&checkpin=1&client=ssologin.js%28v1.4.18%29&_=1458836718537'
            pre_response=requests.get(pre_login_url).text
            pre_content_regex=r'\((.*?)\)'
            patten=re.search(pre_content_regex, pre_response)
            nonce=None
            pubkey=None
            servertime=None
            rsakv=None
            if patten.groups():
                pre_content=patten.group(1)
                pre_result=json.loads(pre_content)
                nonce=pre_result.get("nonce")
                pubkey=pre_result.get('pubkey')
                servertime=pre_result.get('servertime')
                rsakv=pre_result.get("rsakv")
            return nonce, pubkey, servertime, rsakv

        def generate_form_data(nonce, pubkey, servertime, rsakv, username, password):
            rsa_public_key=int(pubkey, 16)
            key=rsa.PublicKey(rsa_public_key, 65537)
            message=str(servertime) + '\t' + str(nonce) + '\n' + str(password)
            passwd=rsa.encrypt(bytes(message, encoding='utf-8'), key)
            passwd=binascii.b2a_hex(passwd)
            username=urllib2.quote(username)
            username=base64.encodestring(bytes(username, encoding='utf-8'))
            form_data={'entry': 'weibo', 'gateway': '1', 'from': '', 'savestate': '7', 'useticket': '1', 'pagerefer': 'http://weibo.com/p/1005052679342531/home?from=page_100505&mod=TAB&pids=plc_main', 'vsnf': '1', 'su': username, 'service': 'miniblog', 'servertime': servertime, 'nonce': nonce, 'pwencode': 'rsa2', 'rsakv': rsakv, 'sp': passwd, 'sr': '1366*768', 'encoding': 'UTF-8', 'prelt': '115', 'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack', 'returntype': 'META'}
            form_data=urllib.parse.urlencode(form_data)
            form_data = bytes(form_data, encoding='utf-8')
            return form_data

        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        headers = ("User-Agent", 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0')
        cookie = cookielib.MozillaCookieJar(cookie_file)
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        opener.addheaders.append(headers)
        nonce, pubkey, servertime, rsakv = pre_login()
        username = input("username:")
        password = input("password:")
        req = opener.open(url, generate_form_data(nonce, pubkey, servertime, rsakv, username, password))
        redirect_result = req.read()
        login_pattern = r'location.replace\(\\\'(.*?)\\\'\)'
        # print(redirect_result)
        login_url = re.search(login_pattern, str(redirect_result)).group(1)
        # print(login_url)
        opener.open(login_url).read()
        cookie.save(cookie_file, ignore_discard=True, ignore_expires=True)

        return

    @staticmethod
    def get_at_list():
        at_list = (
            "我玩98k",
        )
        return ''.join(f'@{x}' for x in at_list)

    def add_post(self, text, image_path=None):
        """add weibo post blog
        :param text: text msg
        :param image_path: path to local image
        """
        post_url = 'https://weibo.com/aj/mblog/add'
        post_data = {
            "text": text + " " + self.__cur_str_date(),
        }

        if image_path:
            pid = WeiboImage().upload_image_to_weibo(image_path)
            # pid = '69405af6gy1fx8x9ebqbgj20t42eaha8'
            if pid:
                post_data['pic_id'] = pid

        res_result = self.__send_http_request(url=post_url, data=post_data)
        if res_result:
            result = json.loads(res_result)
            result_msg = self.__WEIBO_CODE.get(result.get('code')) or result.get('msg')
        else:
            result_msg = 'post failed!'
        logging.info(result_msg)

        return None

    @staticmethod
    def __cur_str_date():
        return '【' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + '】'


class WeiboImage:

    """weibo image handler
    1. upload image to weibo: return weibo pid or image url.
    2. get weibo image url by pid: return full image url.
    """

    def __init__(self):
        weibo = Weibo()
        self.__send_http_request = weibo.send_http_request

    def upload_image_to_weibo(self, image_path):
        """
        upload image to weibo and get weibo image source pid
        :param image_path:
        :return: weibo imgage pid or image url
        """
        import base64

        image_url = 'http://picupload.service.weibo.com/interface/pic_upload.php?mime=image%2Fjpeg&data=base64&url=0&markpos=1&logo=&nick=0&marks=1&app=miniblog'
        b = base64.b64encode(open(image_path, 'rb').read())
        data = {
            'b64_data': b,
        }
        res_result = self.__send_http_request(url=image_url, data=data)
        if res_result:
            html = res_result.decode().strip().strip('\n')
            image_result = re.sub(r"<meta.*</script>", "", html, flags=re.S)
            image_result = json.loads(image_result)
            pid = image_result.get('data').get('pics').get('pic_1').get('pid')
            logging.info('got image, id=%s' % pid)
        else:
            pid = None
        # return 'http://ww3.sinaimg.cn/large/%s'%image_id
        return pid

    @staticmethod
    def get_weibo_image_url(pid):
        """get full size weibo image url by pid"""
        return f'http://ww3.sinaimg.cn/large/{pid}'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    tasklist = [realtimehot]
    # tasklist = ['https://s.weibo.com/top/summary?cate=realtimehot']
    result = [crawl(task) for task in tasklist]
    logging.info('got %s news.' % len(*result))
    format_result = format_to_html(*result)
    # logging.info(format_result)
    # send_msg(msg=format_result, attach_file=[{"filename": 'out.jpg', "body": open('out.jpg', 'rb').read()}])

    # convert to image
    convert_html_to_image(html=format_result)
    # convert_url_to_image(url='https://www.diyidan.com')

    # send a weibo dialog
    weibo = Weibo()
    # weibo.add_post(format_to_md(*result))
    # weibo.add_post(f'微博实时热搜榜 {date.today()}')
    weibo.add_post(text=f'微博实时热搜榜{weibo.get_at_list()}', image_path='out.jpg')
