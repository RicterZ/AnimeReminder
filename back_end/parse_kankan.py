#coding: utf-8
import re
import urllib2
import json
from django.utils.timezone import now
from back_end.parse_bilibili import get_bilibili_anime_detail, get_real_name


def get_anime_detail(aid, get_bilibili=True):
    """
    参考:
    http://data.pad.kankan.com/mobile/detail/74/74031.json
    http://data.pad.kankan.com/mobile/sub_detail/74/74031.json
    """
    aid = str(aid)
    anime_data = {}
    bilibili_data = {}
    is_end = False
    detail_url = 'http://data.pad.kankan.com/mobile/detail/%s/%s.json'
    detail_url = detail_url % (aid[:2], aid)

    try:
        result = urllib2.urlopen(detail_url).read()
        if result:
            anime_data = json.loads(result)
            is_end = True if anime_data.get('totalEpisodeCount') else False

        if get_bilibili:
            bilibili_data = get_bilibili_anime_detail(urllib2.quote(anime_data['title'].encode('utf-8')))

        anime_final_data = dict({
            'aid': aid,
            'name': anime_data['title'],
            'episode': anime_data['episodeCount'],
            'intro': anime_data['intro'],
            'is_end': is_end,
            'poster_link': anime_data['poster'],
            'updated_time': now()
        }, **bilibili_data)

        if anime_final_data['episode'] < anime_final_data['bilibili_bgmcount']:
            anime_final_data['episode'] = anime_final_data['bilibili_bgmcount']

        return anime_final_data

    except urllib2.HTTPError:
        return None

