# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""update for looter"""


import os
import asyncio
import aiohttp
from fake_useragent import UserAgent
from looter.utils import get_img_name

from app.database.mm import mm_db


def save_mm(name, url, ori_url, source):
    """save mm image to sql"""
    add_item = {
        "name": name,
        "url": url,
        "ori_url": ori_url,
        "type": 'model',
        "creator": 0,
        "source": source,
    }
    mm_db.add_mm(item=add_item)


async def async_save_img(url: str, random_name=False, headers=None, proxy=None, cookies=None, save_path=None):
    """Save an image in an async style.

    Args:
        url (str): The url of the site.
        random_name (int, optional): Defaults to False. If names of images are duplicated, use this.
        headers (optional): Defaults to fake-useragent, can be customed by user.
        proxy (optional): Defaults to None, can be customed by user.
        cookies (optional): Defaults to None, if needed, use read_cookies().
        save_path (optional): Defaults to None, can be customed by user.
    """
    if not headers:
        headers = {'User-Agent': UserAgent().random}
    name = get_img_name(url, random_name=random_name)
    if save_path is not None and os.path.isdir(save_path):
        abs_name = os.path.join(save_path, name)
    else:
        abs_name = name
    with open(abs_name, 'wb') as f:
        async with aiohttp.ClientSession(cookies=cookies) as ses:
            async with ses.get(url, headers=headers, proxy=proxy) as res:
                data = await res.read()
                f.write(data)
                print(f'Saved {name}')

    # save to sql
    save_mm(name=name, url=name, ori_url=url, source='http://www.mm131.com')


def async_save_imgs(urls: list, random_name=False, headers=None, proxy=None, cookies=None, save_path=None):
    """
    Download images from links in an async style.
    """
    loop = asyncio.get_event_loop()
    result = [async_save_img(url, random_name=random_name,
                             headers=headers, proxy=proxy, cookies=cookies, save_path=save_path) for url in urls]
    loop.run_until_complete(asyncio.wait(result))
