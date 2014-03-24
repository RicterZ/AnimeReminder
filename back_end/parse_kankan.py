#coding: utf-8
from django.utils.timezone import now
import urllib2
import json


def get_kankan_anime_detail(aid):
    """
    参考:
    http://data.pad.kankan.com/mobile/detail/74/74031.json
    http://data.pad.kankan.com/mobile/sub_detail/74/74031.json
    """
    aid = str(aid)
    detail_url = 'http://data.pad.kankan.com/mobile/detail/%s/%s.json'
    detail_url = detail_url % (aid[:2], aid)

    result = urllib2.urlopen(detail_url).read()
    if result:
        anime_data = json.loads(result)
        is_end = True if anime_data.get('totalEpisodeCount') else False
    else:
        anime_data = get_kankan_anime_detail_by_win(aid)
        is_end = False

    return {
        'aid': aid,
        'name': anime_data['title'],
        'intro': anime_data['intro'],
        'is_end': is_end,

        # 这里默认先不实现
        'bilibili_aid': 0,
        'bilibili_link': '',
        'bilibili_bgmcount': 0,
        'bilibili_season': 1,

        'poster_link': anime_data['poster'],
        'updated_time': now()
    }


def get_kankan_anime_detail_by_win(aid):
    """
    参考 https://github.com/RicterZ/AnimeReminder/blob/master/lib/anime.py
    下载 lua 文件然后解析
    """
    return {}


def search_anime(name):
    return []


def search_anime_by_win(name):
    return []