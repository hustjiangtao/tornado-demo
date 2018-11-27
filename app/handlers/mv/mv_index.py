# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""mv"""


from collections import defaultdict

from app.handlers.base_handler import BaseHandler
from app.lib.do_cache import do_temp_cache

from app.database.user import user_db
from app.database.doc import doc_db


class MvIndexHandler(BaseHandler):

    """mv handler"""

    # @do_temp_cache(3600, with_user=False)
    def get(self):
        """video index page"""
        offset = self.get_query_argument('offset', None) or 0
        limit = self.get_query_argument('limit', None) or 100

        # docs = doc_db.get_sorted_docs_by_read(offset=offset, limit=limit)
        # user_ids = {x.get('author') for x in docs}
        # users = user_db.get_users_by_ids(ids=user_ids)
        # user_name_dict = {x.get('id'): x.get('name') for x in users}
        # items_dict = defaultdict(list)
        # if docs:
        #     for x in docs:
        #         x['author'] = user_name_dict.get(x.get('author')) or '无名达人'
        #         items_dict[x.get('category')].append(x)
        #     result = dict(sorted(items_dict.items(), key=lambda x: x[0]))
        # else:
        #     result = {}

        result = {
            # banner count = 5, (1 large, 4 small)
            "banner_list": [
                {
                    "vid_data": {
                        "create_time": '4 Months ago',
                        "source_ori": 'youtube',
                        "view_count": '4481',
                    },
                    "vid_detail": {
                        "thumb_sm": 'images/main-vid-image-md-1.jpg',
                        "thumb_lg": 'images/main-vid-image-smmd-1.jpg',
                        "title": 'Gladiators Fighting',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                },
                {
                    "vid_data": {
                        "create_time": 'A month ago',
                        "source_ori": 'dailymotion',
                        "view_count": '4000',
                    },
                    "vid_detail": {
                        "thumb_sm": 'images/main-vid-image-mds-1.jpg',
                        "thumb_lg": 'images/main-vid-image-sm-1.jpg',
                        "title": 'Awesome Film Performance',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                },
                {
                    "vid_data": {
                        "create_time": 'A month ago',
                        "source_ori": 'youtube',
                        "view_count": '4000',
                    },
                    "vid_detail": {
                        "thumb_sm": 'images/main-vid-image-mds-2.jpg',
                        "thumb_lg": 'images/main-vid-image-sm-2.jpg',
                        "title": 'Awesome Film Performance',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                },
                {
                    "vid_data": {
                        "create_time": 'A month ago',
                        "source_ori": 'vimeo',
                        "view_count": '4000',
                    },
                    "vid_detail": {
                        "thumb_sm": 'images/main-vid-image-mds-3.jpg',
                        "thumb_lg": 'images/main-vid-image-sm-3.jpg',
                        "title": 'Awesome Film Performance',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                },
                {
                    "vid_data": {
                        "create_time": 'A month ago',
                        "source_ori": 'dailymotion',
                        "view_count": '4000',
                    },
                    "vid_detail": {
                        "thumb_sm": 'images/main-vid-image-mds-4.jpg',
                        "thumb_lg": 'images/main-vid-image-sm-4.jpg',
                        "title": 'Awesome Film Performance',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                },
            ],
            # lasted count = 9
            "lasted_list": [
                {
                    "vid_data": {
                        "create_time": 'A Months ago',
                        "source_ori": 'youtube',
                        "view_count": '410',
                    },
                    "vid_detail": {
                        "thumb_sm": f'images/latest-vid-img-{i}.jpg',
                        "thumb_lg": '',
                        "title": 'Gladiators Fighting',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                } for i in range(1, 10)
            ],
            # most_viewd count = 6
            "most_viewd_list": [
                {
                    "vid_data": {
                        "create_time": '4 Months ago',
                        "source_ori": 'youtube',
                        "view_count": '410',
                    },
                    "vid_detail": {
                        "thumb_sm": f'images/latest-vid-img-{i}.jpg',
                        "thumb_lg": '',
                        "title": 'Gladiators Fighting',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                } for i in range(7, 13)
            ],
            # sports count = 4
            "sports_list": [
                {
                    "vid_data": {
                        "create_time": '4 Months ago',
                        "source_ori": 'youtube',
                        "view_count": '410',
                    },
                    "vid_detail": {
                        "thumb_sm": f'images/sport-vid-img-{i}.jpg',
                        "thumb_lg": '',
                        "title": 'Gladiators Fighting',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                } for i in range(1, 5)
            ],
            # hd count = 1
            "hd_list": [
                {
                    "vid_data": {
                        "create_time": '4 Months ago',
                        "source_ori": 'youtube',
                        "view_count": '410',
                    },
                    "vid_detail": {
                        "thumb_sm": 'images/hd-vid-img-1.jpg',
                        "thumb_lg": '',
                        "title": 'Gladiators Fighting',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                },
            ],
            # 3d count = 2
            "3d_list": [
                {
                    "vid_data": {
                        "create_time": '4 Months ago',
                        "source_ori": 'youtube',
                        "view_count": '410',
                    },
                    "vid_detail": {
                        "thumb_sm": f'images/hd-vid-sm-img-{i}.jpg',
                        "thumb_lg": '',
                        "title": 'Gladiators Fighting',
                        "desc": 'abcdddd',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                } for i in range(1, 3)
            ],
            # sidebar_most_liked count = 4
            "sidebar_most_liked_list": [
                {
                    "vid_data": {
                        "create_time": '4 Months ago',
                        "source_ori": 'youtube',
                        "view_count": '410',
                        "comment_count": '10',
                    },
                    "vid_detail": {
                        "thumb_sm": f'images/most-liked-img-s{i}.jpg',
                        "thumb_lg": '',
                        "title": 'Gladiators Fighting',
                        "desc": 'abcdddd',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                } for i in range(1, 5)
            ],
            # sidebar_most_viewd count = 2
            "sidebar_most_viewd_list": [
                {
                    "vid_data": {
                        "create_time": '4 Months ago',
                        "source_ori": 'youtube',
                        "view_count": '410',
                        "comment_count": '10',
                    },
                    "vid_detail": {
                        "thumb_sm": f'images/most-viewd-{i}.jpg',
                        "thumb_lg": '',
                        "title": 'Gladiators Fighting',
                        "desc": 'abcdddd',
                        "detail_url": 'video-detail.html',
                        "play_url": 'video-detail.html',
                    },
                    "vid_author": {
                        "name": 'Admin',
                    },
                } for i in range(1, 3)
            ],
            # sidebar_tag count = ~
            "sidebar_tag_list": ['3D', 'Animals &amp; Birds', 'HD', 'Horror', 'Art', 'Self', 'HD Songs', 'Comedy'],
        }

        data = {
            "offset": offset,
            "limit": limit,
            "result": result,
        }
        self.render('mv/index.html', data=data)

    def options(self):
        self.write('GET')
