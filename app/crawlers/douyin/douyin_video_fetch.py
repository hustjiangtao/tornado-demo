# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""douyin video fetch"""


import traceback
import time
import logging
import requests
from collections import OrderedDict

from app.crawlers.douyin.fetch_douyin_to_sql import fetch_handler


# 需要爬取的用户信息(用户ID:(标签，版区，昵称))
USER_INFO = {
    # 已跑完的用户先注释
    58653085886: (u'绝地求生', u'吃鸡游戏', u'浩轩（搞笑吃鸡）', 20),  # 浩轩（搞笑吃鸡）
    62955603441: (u'绝地求生', u'吃鸡游戏', u'吃鸡搞笑视频（绝地求生）', 20),  # 吃鸡搞笑视频（绝地求生）
    98459103206: (u'绝地求生', u'吃鸡游戏', u'绝地求生吃鸡搞笑视频', 20),  # 绝地求生吃鸡搞笑视频
    97543940715: (u'绝地求生', u'吃鸡游戏', u'叮当（搞笑游戏）', 20),  # 叮当（搞笑游戏）
    58197423146: (u'王者荣耀', u'王者荣耀', u'周斌玩游戏', 20),  # 周斌玩游戏
    83096184229: (u'王者荣耀', u'王者荣耀', u'王者荣耀', 20),  # 王者荣耀
    59359411419: (u'王者荣耀', u'王者荣耀', u'王者荣耀林颜', 20),  # 王者荣耀林颜
    72877898406: (u'王者荣耀', u'王者荣耀', u'王者荣耀创意君', 20),  # 王者荣耀创意君
    76324608011: (u'手机游戏', u'手机游戏', u'剑侠世界2', 20),  # 剑侠世界2
    97523645652: (u'逆水寒', u'游戏', u'逆水寒', 20),  # 逆水寒
    96540684488: (u'英雄联盟', u'游戏', u'英雄联盟 陈不奶', 20),  # 英雄联盟 陈不奶
    97392049171: (u'英雄联盟', u'游戏', u'英雄联盟皮肤', 20),  # 英雄联盟皮肤
    99684495739: (u'游戏推荐', u'游戏', u'游戏大坑', 20),  # 游戏大坑
    96752247209: (u'手机游戏', u'手机游戏', u'十三叔说游戏', 20),  # 十三叔说游戏
    95910596570: (u'高能时刻', u'游戏', u'高能游戏君', 20),  # 高能游戏君
    95174729341: (u'手游推荐', u'手机游戏', u'转角遇到游戏姬', 20),  # 转角遇到游戏姬
    84572362452: (u'绝地求生', u'吃鸡游戏', u'娱游游戏', 20),  # 娱游游戏
    65097903853: (u'绝地求生', u'吃鸡游戏', u'AK游戏解说', 20),  # AK游戏解说
    95437437303: (u'绝地求生', u'吃鸡游戏', u'大吉大利今晚吃鸡', 20),  # 大吉大利今晚吃鸡
    105217695785: (u'绝地求生', u'吃鸡游戏', u'小信吃鸡', 20),  # 小信吃鸡
    94781593931: (u'绝地求生', u'吃鸡游戏', u'老赫晨_绝地求生搞笑吃鸡', 20),  # 老赫晨_绝地求生搞笑吃鸡
}
USER_INFO = OrderedDict(sorted(USER_INFO.items(), key=lambda t: t[1][3]))

HEADERS = {
    "user-agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}


class Utils:

    @classmethod
    def replace_emoji(cls, content):
        if not content:
            return

        import re
        try:
            # myre = re.compile(ur'[\U00010000-\U0010ffff\u202A-\u202E\u0200-\u0fff]')
            myre = re.compile(r'[\U00010000-\U0010ffff\u202A-\u202E]')
        except re.error:
            # UCS-2 build
            myre = re.compile(r'[\uD800-\uDBFF][\uDC00-\uDFFF]')

        try:
            content = myre.sub('', content)
            content = content.strip()
        except Exception as e:
            logging.warning(traceback.format_exc())

        return content


def get_all_user_videos():
    """
    逐个对用户进行视频抓取
    """
    for uid in USER_INFO.keys():
        logging.info("start for user %s" % uid)

        has_more = 1
        max_cursor = 0
        while has_more:
            content = None
            user_url = 'https://aweme.snssdk.com/aweme/v1/aweme/post/'
            params = {
                "iid": 51054222669,
                "device_type": 'iPhone10,3',
                "user_id": uid,
                "count": 12,
                "max_cursor": max_cursor,
                "aid": 1128,
            }
            try:
                response = requests.get(url=user_url, params=params, headers=HEADERS)
                if response.status_code != 200:
                    break
                content = response.json()
            except Exception as e:
                logging.error(traceback.format_exc())

            if not content:
                break
            if content.get("aweme_list") and isinstance(content["aweme_list"], list):
                aweme_list = content.get('aweme_list')
                logging.info(len(aweme_list))
                for aweme in aweme_list:
                    video = aweme.get('video')
                    if not video:
                        continue
                    video_id=aweme.get('aweme_id')
                    video_url=video.get('play_addr').get('url_list')[0]
                    video_image_url=video.get('cover').get('url_list')[0]
                    video_duration=video.get('duration')
                    video_desc = aweme.get('desc')
                    video_timestamp=aweme.get('create_time')
                    video_width=video.get('play_addr').get('width')
                    video_height=video.get('play_addr').get('height')
                    # print 'get video+++', video_id, video_url, video_image_url, video_timestamp

                    # download video
                    video_content = None
                    try:
                        response=requests.get(url=video_url, headers=HEADERS)
                        if response.status_code!=200:
                            continue
                        video_content = response.content
                    except Exception as e:
                        logging.error(traceback.format_exc())
                    if not video_content:
                        continue
                    video_view_url = fetch_handler.save_video_to_target_path(name=video_desc, content=video_content)
                    if not video_view_url:
                        continue

                    # download cover image
                    img_content = None
                    try:
                        response=requests.get(url=video_image_url, headers=HEADERS)
                        if response.status_code!=200:
                            continue
                        img_content = response.content
                    except Exception as e:
                        logging.error(traceback.format_exc())
                    if not img_content:
                        continue
                    cover_image_url = fetch_handler.save_image_to_target_path(name=video_desc, content=img_content)

                    video_info_dict = {
                        "name": video_desc,
                        "url": video_view_url,
                        "ori_url": video_url,
                        "cover_url": cover_image_url,
                        "info": video_desc,
                        "source": 'douyin',
                        "duration": video_duration,
                        "size": len(content),
                        "width": video_width,
                        "height": video_height,
                    }
                    result = fetch_handler.save_video_to_sql(video=video_info_dict)
                    if result:
                        logging.info('save video to sql complete...id=%s', result)
                    # get_video_details_and_save(uid, video_id, video_url, video_image_url, video_timestamp, video_duration, video_desc)
            has_more = content.get("has_more", 0)
            max_cursor = content.get("max_cursor", 0)


def get_video_details_and_save(kuaishou_user_id, video_id, video_url, video_image_url, video_timestamp, video_duration, video_desc):
    """
    获取视频信息，并上传评论
    :param kuaishou_user_id: 快手用户ID
    :param video_id: 快手videoID
    :param video_url: 快手videoURL
    :param video_image_url: 快手图片地址
    :param video_timestamp: 视频发布时间戳
    :return:
    """
    # return
    url = video_url

    # 获取视频总时间，如果视频总时间超过300秒，则不进行抓取
    if video_duration > 300 * 1000:
        return None
    video_introduction = Utils.replace_emoji(video_desc or u'')

    has_more = 1
    cursor = 0
    while has_more:
        comment_message = None
        per_page = 20
        try:
            comment_url = 'https://api.amemv.com/aweme/v2/comment/list/'
            params = {
                "aweme_id": video_id,
                "count": per_page,
                "cursor": cursor,
            }
            response = requests.get(url=comment_url, params=params, headers=HEADERS)
            if response.status_code != 200:
                break
            comment_message = response.json()
        except Exception as e:
            logging.error(traceback.format_exc())

        if not comment_message:
            break
        has_more = comment_message.get("has_more", 0)
        cursor = comment_message.get("cursor", cursor+per_page)
        comment_list = comment_message.get("comments")
        if not comment_list or not isinstance(comment_list, list):
            break

        for comment in comment_list:
            comment_content = comment.get("text", '')
            comment_content = Utils.replace_emoji(comment_content)
            if not comment_content:
                continue
            if comment_content.isdigit():
                continue
            if 'www' in comment_content or 'http' in comment_content:
                continue
            # print '+++++comment id', comment_id
    # 抓取每个视频之间间隔 2 秒
    time.sleep(2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("job start...")
    get_all_user_videos()
    logging.info('done.')
