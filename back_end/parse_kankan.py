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

    str_aid = str(aid)
    aid_url = str_aid[0] + str_aid[1] + '/' + str_aid + '.json'
    detail_url = 'http://data.pad.kankan.com/mobile/detail/' + aid_url
    sdetail_url = 'http://data.pad.kankan.com/mobile/sub_detail/' + aid_url

    result = urllib2.urlopen(detail_url).read()
    jobject = json.loads(result)
    name = jobject['title']
    intro = jobject['intro']
    poster_link = jobject['poster']
    is_end = False
    if jobject['episodeCount'] == jobject['totalEpisodeCount']:
        is_end = True

    #result = urllib2.urlopen(sdetail_url).read()
    #jobject = json.loads(result)

    return {
        'aid': aid,
        'name': name,
        'intro': intro,
        'is_end': is_end,

        # 这里默认先不实现
        'bilibili_aid': 0,
        'bilibili_link': '',
        'bilibili_bgmcount': 0,
        'bilibili_season': 1,

        'poster_link': poster_link,
        'updated_time': now()
    }

