# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""fetch douyin video to sql & display on mv"""


from app.crawlers.spider_world.www_douyin_com import douyin_crawl


class FetchHandler:

    @classmethod
    def save_file_and_get_file_url(cls, file_content, file_type, file_extension=None):
        """
        save file and get static url for image or video
        :param file_type: file type, eg: img, video
        :return: str, file url without prefix
        """
        from pathlib import Path
        from datetime import date
        from app.config import STATIC_DIR

        file_extensions = {
            "img": 'jpg',
            "video": 'mp4',
        }

        today = date.today()
        static_dir = Path(STATIC_DIR.get('base'))
        file_prefix = f'mv/{file_type}/{today.year}/{today.month}/{today.day}/'

        if not (static_dir / file_prefix).exists():
            (static_dir / file_prefix).mkdir(parents=True)

        file_url = file_prefix + cls.get_random_string(16) + '.' + (file_extension or file_extensions.get(file_type))
        with (static_dir / file_url).open('wb') as f:
            f.write(file_content)

        return f'/{file_url}'

    @classmethod
    def save_image_to_target_path(cls, name, content):
        return cls.save_file_and_get_file_url(file_content=content, file_type='img')

    @classmethod
    def save_video_to_target_path(cls, name, content):
        return cls.save_file_and_get_file_url(file_content=content, file_type='video')

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
