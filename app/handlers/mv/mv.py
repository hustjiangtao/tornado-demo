# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""MV detail"""


from app.handlers.base_handler import BaseHandler
from app.handlers.base_handler import authenticated
from app.lib.do_cache import do_temp_cache

from app.database.user import user_db
from app.database.mv import mv_db

from app.lib.system_code import SUCCESS
from app.lib.system_code import PARAMS_MISS


class MvHandler(BaseHandler):

    """mv handler"""

    @authenticated
    def post(self):
        """doc add api"""
        title = self.get_body_argument('title', None)
        category = self.get_body_argument('category', None)
        tags = self.get_body_argument('tags', None)
        content = self.get_body_argument('content', None)

        code = SUCCESS
        data = None

        if not all([title, category, content]):
            code = PARAMS_MISS
        else:
            if tags:
                tags = tags.strip()
            add_item = {
                "title": title,
                "category": category,
                "tags": tags,
                "content": content,
            }
            result = doc_db.add_doc(item=add_item)
            if result:
                data = {
                    "id": result,
                }

        self.render_json(code=code, data=data)

    @authenticated
    def delete(self):
        pass

    @authenticated
    def put(self):
        """demo update api"""
        _id = self.get_body_argument('id', None)
        title = self.get_body_argument('title', None)
        category = self.get_body_argument('category', None)
        tags = self.get_body_argument('tags', None)
        content = self.get_body_argument('content', None)

        code = SUCCESS
        data = None

        if not all([_id, title, category, content]):
            code = PARAMS_MISS
        else:
            if tags:
                tags = tags.strip()
            update_item = {
                "title": title,
                "category": category,
                "tags": tags,
                "content": content,
            }
            result = doc_db.update_doc(_id=_id, item=update_item)
            if result:
                data = {
                    "result": True,
                }

        self.render_json(code=code, data=data)

    # @authenticated
    # @do_temp_cache(7*3600, with_user=False)
    def get(self, _id):
        """detail info page"""
        item = mv_db.get_mv_by_id(_id=_id)

        related_mvs = mv_db.get_sorted_mvs_by_rate(offset=0, limit=3, order_by='rate')
        most_viewed_mvs = mv_db.get_sorted_mvs_by_rate(offset=0, limit=2, order_by='rate')
        most_liked_mvs = mv_db.get_sorted_mvs_by_rate(offset=0, limit=2, order_by='like')

        all_mvs = [*related_mvs, *most_viewed_mvs, *most_liked_mvs, item]
        user_ids = {x.get('creator') for x in all_mvs}
        users = user_db.get_users_by_ids(ids=user_ids)
        user_name_dict = {x.get('id'): x.get('name') for x in users}
        if all_mvs:
            for x in all_mvs:
                x['creator'] = user_name_dict.get(x.get('creator')) or '无名达人'

        current_vid = self.__get_mv_obj(item)
        related_list = list(map(self.__get_mv_obj, related_mvs))
        most_viewed_list = list(map(self.__get_mv_obj, most_viewed_mvs))
        most_liked_list = list(map(self.__get_mv_obj, most_liked_mvs))
        tags_list = ['3D', 'Animals &amp; Birds', 'HD', 'Horror', 'Art', 'Self', 'HD Songs', 'Comedy']

        result = {
            # current vid
            "vid": current_vid,
            # related count = 3
            "related_list": related_list or [
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
            "result": result,
        }
        self.render('mv/video-detail.html', data=data)

    # @authenticated
    def options(self):
        self.write('POST,PUT,GET')

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

