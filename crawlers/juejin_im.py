# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import time
from datetime import timedelta, datetime

try:
    from HTMLParser import HTMLParser
    from urlparse import urljoin, urldefrag
except ImportError:
    from html.parser import HTMLParser
    from urllib.parse import urljoin, urldefrag

from tornado import httpclient, gen, ioloop, queues

from lib.utils import json_decode
from database.post import post_db

page = 0
base_url = 'https://search-merger-ms.juejin.im/v1/search?query={query}&page={page}&raw_result=false&src=web'
concurrency = 10


def get_current_url(query='python', page=0):
    return base_url.format(query=query, page=page)


@gen.coroutine
def get_links_from_url(url):
    """Download the page at `url` and parse it for links.

    Returned links have had the fragment after `#` removed, and have been made
    absolute so, e.g. the URL 'gen.html#tornado.gen.coroutine' becomes
    'http://www.tornadoweb.org/en/stable/gen.html'.
    """
    try:
        response = yield httpclient.AsyncHTTPClient().fetch(url)
        print('fetched %s' % url)

        html = response.body if isinstance(response.body, str) \
            else response.body.decode()
        html = json_decode(html)
        urls = get_content(html)
        print(len(urls))
    except Exception as e:
        print('Exception: %s %s' % (e, url))
        raise gen.Return([])

    raise gen.Return(urls)


def get_content(html):
    if not isinstance(html, dict):
        return []

    data = html.get('d')
    result = [{
        "title": x.get('title'),
        "content": x.get('content'),
        "author": x.get('user').get('username') or 'unknown',
        "source": 'juejin',
        "source_id": x.get('objectId'),
        "original_url": x.get('originalUrl'),
        "collection_count": x.get('collectionCount'),
        "comments_count": x.get('commentsCount'),
        "create_time": datetime.strptime(x.get('createdAt').split('.')[0], '%Y-%m-%dT%H:%M:%S'),
    } for x in data]
    return result


def filter_fetched_content(result):
    fetched_original_urls = post_db.get_all_crawler_original_urls()
    fetched = set(fetched_original_urls)
    return [x for x in result if x.get('original_url') not in fetched]


@gen.coroutine
def main():
    q = queues.Queue()
    start = time.time()
    fetching, fetched = set(), set()
    results = []

    @gen.coroutine
    def fetch_url(page):
        current_url = yield q.get()
        try:
            if current_url in fetching:
                return

            print('fetching %s' % current_url)
            fetching.add(current_url)
            contents = yield get_links_from_url(current_url)
            results.extend(contents)
            fetched.add(current_url)

            if contents:
                next_url = get_current_url(page=page)
                yield q.put(next_url)

        finally:
            q.task_done()

    @gen.coroutine
    def worker():
        global page
        while True:
            page += 1
            yield fetch_url(page)
            # time.sleep(0.5)

    q.put(get_current_url(page=0))

    # Start workers, then wait for the work queue to be empty.
    for _ in range(concurrency):
        worker()
    yield q.join(timeout=timedelta(seconds=300))
    assert fetching == fetched
    print('Done in %d seconds, fetched %s URLs.' % (
        time.time() - start, len(fetched)))

    results = filter_fetched_content(results)
    print(len(results))
    post_db.add_crawler_posts(items=results)


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)