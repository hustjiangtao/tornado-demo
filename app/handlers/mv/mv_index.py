# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""mv"""


from collections import defaultdict

from app.handlers.base_handler import BaseHandler
from app.lib.do_cache import do_temp_cache

from app.database.user import user_db
from app.database.mv import mv_db


class MvIndexHandler(BaseHandler):

    """mv handler"""

    @do_temp_cache(60*10, with_user=False)
    def get(self):
        """video index page"""
        offset = self.get_query_argument('offset', None) or 0
        limit = self.get_query_argument('limit', None) or 100

        lasted_mvs = mv_db.get_mvs(offset=offset, limit=limit, order_by='create_time')
        most_viewed_mvs = mv_db.get_sorted_mvs_by_rate(offset=offset, limit=limit, order_by='rate')
        most_liked_mvs = mv_db.get_sorted_mvs_by_rate(offset=offset, limit=limit, order_by='like')

        all_mvs = [*lasted_mvs, *most_viewed_mvs, *most_liked_mvs]
        user_ids = {x.get('creator') for x in all_mvs}
        users = user_db.get_users_by_ids(ids=user_ids)
        user_name_dict = {x.get('id'): x.get('name') for x in users}
        if all_mvs:
            for x in all_mvs:
                x['creator'] = user_name_dict.get(x.get('creator')) or '无名达人'

        lasted_list = list(map(self.__get_mv_obj, lasted_mvs))
        most_viewed_list = list(map(self.__get_mv_obj, most_viewed_mvs))
        most_liked_list = list(map(self.__get_mv_obj, most_liked_mvs))
        tags_list = ['3D', 'Animals &amp; Birds', 'HD', 'Horror', 'Art', 'Self', 'HD Songs', 'Comedy']

        result = {
            # banner count = 5, (1 large, 4 small)
            # "banner_list": [
            #     {
            #         "vid_data": {
            #             "create_time": '4 Months ago',
            #             "source_ori": 'youtube',
            #             "view_count": '4481',
            #         },
            #         "vid_detail": {
            #             "thumb_sm": 'images/main-vid-image-md-1.jpg',
            #             "thumb_lg": 'images/main-vid-image-smmd-1.jpg',
            #             "title": 'Gladiators Fighting',
            #             "detail_url": 'video-detail.html',
            #             "play_url": 'video-detail.html',
            #         },
            #         "vid_author": {
            #             "name": 'Admin',
            #         },
            #     },
            #     {
            #         "vid_data": {
            #             "create_time": 'A month ago',
            #             "source_ori": 'dailymotion',
            #             "view_count": '4000',
            #         },
            #         "vid_detail": {
            #             "thumb_sm": 'images/main-vid-image-mds-1.jpg',
            #             "thumb_lg": 'images/main-vid-image-sm-1.jpg',
            #             "title": 'Awesome Film Performance',
            #             "detail_url": 'video-detail.html',
            #             "play_url": 'video-detail.html',
            #         },
            #         "vid_author": {
            #             "name": 'Admin',
            #         },
            #     },
            #     {
            #         "vid_data": {
            #             "create_time": 'A month ago',
            #             "source_ori": 'youtube',
            #             "view_count": '4000',
            #         },
            #         "vid_detail": {
            #             "thumb_sm": 'images/main-vid-image-mds-2.jpg',
            #             "thumb_lg": 'images/main-vid-image-sm-2.jpg',
            #             "title": 'Awesome Film Performance',
            #             "detail_url": 'video-detail.html',
            #             "play_url": 'video-detail.html',
            #         },
            #         "vid_author": {
            #             "name": 'Admin',
            #         },
            #     },
            #     {
            #         "vid_data": {
            #             "create_time": 'A month ago',
            #             "source_ori": 'vimeo',
            #             "view_count": '4000',
            #         },
            #         "vid_detail": {
            #             "thumb_sm": 'images/main-vid-image-mds-3.jpg',
            #             "thumb_lg": 'images/main-vid-image-sm-3.jpg',
            #             "title": 'Awesome Film Performance',
            #             "detail_url": 'video-detail.html',
            #             "play_url": 'video-detail.html',
            #         },
            #         "vid_author": {
            #             "name": 'Admin',
            #         },
            #     },
            #     {
            #         "vid_data": {
            #             "create_time": 'A month ago',
            #             "source_ori": 'dailymotion',
            #             "view_count": '4000',
            #         },
            #         "vid_detail": {
            #             "thumb_sm": 'images/main-vid-image-mds-4.jpg',
            #             "thumb_lg": 'images/main-vid-image-sm-4.jpg',
            #             "title": 'Awesome Film Performance',
            #             "detail_url": 'video-detail.html',
            #             "play_url": 'video-detail.html',
            #         },
            #         "vid_author": {
            #             "name": 'Admin',
            #         },
            #     },
            # ],
            # lasted count = 9
            "lasted_list": lasted_list or [
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
            "most_viewd_list": most_viewed_list or [
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
            # "sports_list": [
            #     {
            #         "vid_data": {
            #             "create_time": '4 Months ago',
            #             "source_ori": 'youtube',
            #             "view_count": '410',
            #         },
            #         "vid_detail": {
            #             "thumb_sm": f'images/sport-vid-img-{i}.jpg',
            #             "thumb_lg": '',
            #             "title": 'Gladiators Fighting',
            #             "detail_url": 'video-detail.html',
            #             "play_url": 'video-detail.html',
            #         },
            #         "vid_author": {
            #             "name": 'Admin',
            #         },
            #     } for i in range(1, 5)
            # ],
            # hd count = 1
            # "hd_list": [
            #     {
            #         "vid_data": {
            #             "create_time": '4 Months ago',
            #             "source_ori": 'youtube',
            #             "view_count": '410',
            #         },
            #         "vid_detail": {
            #             "thumb_sm": 'images/hd-vid-img-1.jpg',
            #             "thumb_lg": '',
            #             "title": 'Gladiators Fighting',
            #             "detail_url": 'video-detail.html',
            #             "play_url": 'video-detail.html',
            #         },
            #         "vid_author": {
            #             "name": 'Admin',
            #         },
            #     },
            # ],
            # 3d count = 2
            # "3d_list": [
            #     {
            #         "vid_data": {
            #             "create_time": '4 Months ago',
            #             "source_ori": 'youtube',
            #             "view_count": '410',
            #         },
            #         "vid_detail": {
            #             "thumb_sm": f'images/hd-vid-sm-img-{i}.jpg',
            #             "thumb_lg": '',
            #             "title": 'Gladiators Fighting',
            #             "desc": 'abcdddd',
            #             "detail_url": 'video-detail.html',
            #             "play_url": 'video-detail.html',
            #         },
            #         "vid_author": {
            #             "name": 'Admin',
            #         },
            #     } for i in range(1, 3)
            # ],
            # sidebar_most_liked count = 4
            "sidebar_most_liked_list": most_liked_list or [
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
            "sidebar_most_viewd_list": most_viewed_list or [
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
            "sidebar_tag_list": tags_list or ['3D', 'Animals &amp; Birds', 'HD', 'Horror', 'Art', 'Self', 'HD Songs', 'Comedy'],
        }

        data = {
            "offset": offset,
            "limit": limit,
            "result": result,
        }
        self.render('mv/index.html', data=data)

    def options(self):
        self.write('GET')

    def __get_mv_obj(self, obj):
        """
        get mv display obj
        :param obj: dict, mv obj
        :return: dict
        """
        if not all([obj, isinstance(obj, dict)]):
            return {}

        result = {
            "vid_data": {
                "create_time": self.__convert_datetime_to_approximate_form(obj.get('create_time')),
                "source_ori": obj.get('source'),
                "view_count": obj.get('click'),
            },
            "vid_detail": {
                "thumb_sm": obj.get('cover_url'),
                "thumb_lg": obj.get('cover_url'),
                "title": obj.get('name'),
                "desc": obj.get('info'),
                # "detail_url": 'video-detail.html',
                "detail_url": self.reverse_url('mv_detail', obj.get('id')),
                "play_url": obj.get('url'),
            },
            "vid_author": {
                "name": obj.get('creator'),
            },
        }
        return result

    @staticmethod
    def __convert_datetime_to_approximate_form(date_time):
        """
        get display time
        :param date_time: datetime
        :return: str
        """
        from datetime import datetime

        if not isinstance(date_time, datetime):
            return None

        time_delta = datetime.now() - date_time

        if time_delta.days > 28:
            return datetime.strftime(datetime.now(), "%Y-%m-%d")

        if time_delta.days > 1:
            return u"%d天前" % time_delta.days

        if time_delta.seconds >= 3600:
            return u"%d小时前" % (time_delta.seconds / 3600)

        if time_delta.seconds >= 60:
            return u"%d分钟前" % (time_delta.seconds / 60)

        return u"%d秒前" % time_delta.seconds
