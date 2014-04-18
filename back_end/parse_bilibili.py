#coding:utf-8
import urllib2
import json
import re

season_dict = {
    u'零': '0',
    u'一': '1',
    u'二': '2',
    u'三': '3',
    u'四': '4',
    u'五': '5',
}


def parse_season(season_str):
    match_season = re.compile(u'第(.*)季')
    data = match_season.findall(season_str)
    return season_dict[data[0]] if data else 1


def parse_epi(sp_id, season_id=0):
    param = str(sp_id)
    if season_id:
        param += '-' + str(season_id)
    request_url = 'http://www.bilibili.tv/sppage/bangumi-%s-1.html' % param
    result = urllib2.urlopen(request_url).read()
    begin = result.find('<div class="t">')
    end = result.find('</div></a>')
    return 0 if begin == -1 or end == -1 else int(result[begin+18:end-3])


def get_real_name(name):
    url = urllib2.urlopen('http://www.bilibili.tv/sp/%s' % name).url
    return url.split('/')[-1]


def get_bilibili_anime_detail(name):
    api_url = 'http://api.bilibili.tv/sp?title=%s'
    real_title = get_real_name(name)
    sp_data = json.loads(urllib2.urlopen(api_url % real_title).read())
    season, season_id = 0, 0
    if 'code' in sp_data:
        return {}

    sp_id = sp_data['spid']
    if 'season' in sp_data:
        for index in sp_data['season']:
            season_data = sp_data['season'][index]
            if season_data['default']:
                season = parse_season(season_data['season_name'])
                season_id = season_data['season_id']
                break
    season = int(season) if season else 1
    epi = parse_epi(sp_id, season_id)

    return {
        "bilibili_aid": sp_id,
        "bilibili_link": "",
        "bilibili_bgmcount": epi,
        "bilibili_season": season,
    }