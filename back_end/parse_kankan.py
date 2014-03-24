#coding: utf-8
from django.utils.timezone import now


def get_anime_detail(aid):
    """
    参考:
    http://data.pad.kankan.com/mobile/detail/74/74030.json
    http://data.pad.kankan.com/mobile/sub_detail/74/74030.json
    """
    #TODO
    return {
        'aid': aid,
        'name': '轻音少女',
        'intro': '介绍!!!!',
        'is_end': True,

        # 这里默认先不实现
        'bilibili_aid': 0,
        'bilibili_link': '',
        'bilibili_bgmcount': 0,
        'bilibili_season': 1,

        'poster_link': '/xx/xx/xx.jpg',
        'updated_time': now()
    }
