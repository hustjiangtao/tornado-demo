# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""weibo realtimehot"""


import logging
import looter as lt

from datetime import date

from app.lib.mail import send_msg_by_email
from app.scripts.convert_md import convert_md


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
    for news in news_list:
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


def format_to_html(data):
    """format to html"""
    if not data:
        return None
    head = f'## 微博实时热搜榜 {date.today()}\n\n'
    items = '<hr>\n\n'.join([f'- {id} {count} [{word_filter(content)}]({url}) \n\n\t{word_filter(detail)}\n' for id, url, content, count, detail in data])
    foot = '\n'
    module = head + items + foot
    # with open('weibo.md', 'wb') as f:
    #     f.write(bytes(module, encoding='utf-8'))
    module = convert_md(''.join(module))

    return module


def send_msg(msg):
    mail_to = 'hujiangtao@diyidan.com'
    to_name = 'jiangtao'
    subject = f'微博实时热搜榜 {date.today()}'
    return send_msg_by_email(mail_to=mail_to, msg=msg, to_name=to_name, subject=subject)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    tasklist = [realtimehot]
    # tasklist = ['https://s.weibo.com/top/summary?cate=realtimehot']
    result = [crawl(task) for task in tasklist]
    logging.info('got %s news.' % len(*result))
    format_result = format_to_html(*result)
    # logging.info(format_result)
    send_msg(msg=format_result)
