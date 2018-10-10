# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""mm131 images download"""


import looter as lt
from app.crawlers.utils import async_save_imgs


domain = 'http://www.mm131.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'http://www.mm131.com/'  # 必须设定referer，否则会被重定向为qq图片
}


def crawl(url):
    tree = lt.fetch(url)
    imgs = tree.css('dl.list-left dd')[:-1]
    for img in imgs:
        link = img.css('a::attr(href)').extract_first()
        bango = link.split('/')[-1][:-5]
        detail = lt.fetch(link, headers=headers)
        max_page = detail.css('.content-page .page-ch::text').re_first(r'\d+')
        img_urls = [f'http://img1.mm131.me/pic/{bango}/{n}.jpg' for n in range(1, int(max_page)+1)]
        async_save_imgs(img_urls[:3], headers=headers, random_name=True, save_path='/Users/jiangtao.work/Desktop/mm')


if __name__ == '__main__':
    tasklist = [*[f'{domain}/xinggan/'], *[f'{domain}/xinggan/list_6_{n}.html' for n in range(2, 153)]]
    result = [crawl(task) for task in tasklist]