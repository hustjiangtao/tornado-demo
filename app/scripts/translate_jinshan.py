# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import time
from datetime import timedelta

try:
    from HTMLParser import HTMLParser
    from urlparse import urljoin, urldefrag
except ImportError:
    from html.parser import HTMLParser
    from urllib.parse import urljoin, urldefrag

from tornado import httpclient, gen, ioloop, queues

from app.lib.utils import json_decode

base_url = 'http://fy.iciba.com/ajax.php?a=fy&f=auto&t=auto&w='
concurrency = 10
default_data = ['hello', 'world']


def get_data_from_url(url):
    try:
        response = httpclient.HTTPClient().fetch(url)
        # print('fetched %s' % url)

        json_data = json_decode(response.body)
    except Exception as e:
        print('Exception: %s %s' % (e, url))
        return {}

    return json_data


def get_translate_result(data):
    if isinstance(data, dict) and data.get('status') == 0:
        result = data.get('content').get('word_mean')
    else:
        result = []

    return f'{" | ".join(result)}'


def main():
    start = time.time()

    import pyperclip
    copy_data = pyperclip.paste()
    input_data = input("Input words you want to trans: ")
    if input_data:
        copy_data = input_data

    fetched = get_translate([copy_data])
    print(fetched)

    print('Done in %d seconds, fetched %s results.' % (
        time.time() - start, len(fetched)))


def get_translate(data=default_data):
    result = []
    for x in data:
        time.sleep(0.5)
        url = f'{base_url}{x}'
        json_data = get_data_from_url(url)
        content = get_translate_result(json_data)
        # result.append(content)
        result.append(f'{x}: {content}')

    # return f'{" || ".join(result)}'
    return result


__all__ = ['get_translate']


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    # io_loop = ioloop.IOLoop.current()
    # io_loop.run_sync(main)
    main()
