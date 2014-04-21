#coding: utf-8
import re
import urllib2
import json
from django.utils.timezone import now
from back_end.parse_bilibili import get_bilibili_anime_detail


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

    bilibili_data = get_bilibili_anime_detail(anime_data['title'])
    return {
        'aid': aid,
        'name': anime_data['title'],
        'intro': anime_data['intro'],
        'is_end': is_end,

        'poster_link': anime_data['poster'],
        'updated_time': now()
    }.update(bilibili_data)


def get_kankan_anime_detail_by_win(aid):
    """
    参考 https://github.com/RicterZ/AnimeReminder/blob/master/lib/anime.py
    下载 lua 文件然后解析
    """
    return {}


def search_anime(name):
    """
    这里是搜索的接口
    """
    search_url = 'http://mediaso.xmp.kankan.xunlei.com/search.php?keyword=%s'
    match_name = re.compile('\{sname=\"(.*)\".*?imovieid=([\d]+), Type=\"anime\"')

    data = urllib2.urlopen(search_url % name).read()
    anime_data = match_name.findall(data)
    return anime_data

