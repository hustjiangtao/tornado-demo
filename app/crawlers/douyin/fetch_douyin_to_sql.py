# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""fetch douyin video to sql & display on mv"""


from app.crawlers.spider_world.www_douyin_com import douyin_crawl


class FetchHandler:

    @classmethod
    def save_image_to_target_path(cls, name, content):
        import os
        from datetime import date
        from app.config import basedir

        today = date.today()
        static_dir = os.path.join(basedir, 'tmp-mdl')
        file_dir_subfix = f'/mv/imgs/{today.year}/{today.month}/{today.day}'

        file_dir = os.path.join(static_dir, file_dir_subfix)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        name = cls.get_random_string(16)
        file_path = f'{file_dir}/{name}.jpg'
        with open(file_path, 'wb') as f:
            f.write(content)

        file_url = f'{file_dir_subfix}/{name}.jpg'
        return file_url

    @classmethod
    def save_video_to_target_path(cls, name, content):
        import os
        from datetime import date
        from app.config import basedir

        today = date.today()
        static_dir = os.path.join(basedir, 'tmp-mdl')
        file_dir_subfix = f'mv/video/{today.year}/{today.month}/{today.day}'

        file_dir = os.path.join(static_dir, file_dir_subfix)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        name = cls.get_random_string(16)
        file_path = f'{file_dir}/{name}.mp4'
        print(file_path)
        with open(file_path, 'wb') as f:
            f.write(content)

        file_url = f'/{file_dir_subfix}/{name}.mp4'
        return file_url

    def save_video_to_sql(self, video):
        from app.database.mv import mv_db

        item = {
            "name": video.get('name'),
            "url": video.get('url'),
            "ori_url": video.get('ori_url'),
            "cover_url": video.get('cover_url'),
            "type": 'douyin',
            "info": video.get('info'),
            "creator": 0,
            "source": video.get('source'),
            "duration": video.get('duration'),
            "size": video.get('size'),
            "width": video.get('width'),
            "height": video.get('height'),
        }

        result = mv_db.add_mv(item=item)
        return result

    @staticmethod
    def get_random_string(string_length=10):
        """using cryptographic safety random functions"""
        ##TODO compare default random & system_random
        # system_random = random.SystemRandom()
        import random
        import string
        system_random = random

        if string_length < 36:
            return ''.join(system_random.sample(string.ascii_letters + string.digits, string_length))

        return ''.join([system_random.choice(string.ascii_letters + string.digits) for x in range(string_length)])


fetch_handler = FetchHandler()


__all__ = (fetch_handler, )
