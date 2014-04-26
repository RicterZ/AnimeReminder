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
    #TODO: 有可能会有中文集数，或者第⑨集这样的
    bangumi_url = 'http://api.bilibili.cn/spview?spid=%d&season_id=%s&bangumi=1' % \
                  (sp_id, str(season_id) if season_id else '')
    epi_list = json.loads(urllib2.urlopen(bangumi_url).read())['list']

    if not epi_list:
        return 0

    for index in epi_list.keys():
        epi_str = epi_list[index].episoid
        try:
            epi = int(epi_str)
        except ValueError:
            if '-' in epi_str:
                epi = epi_str


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
        "bilibili_link": "http://www.bilibili.tv/sp/%s" % real_title,
        "bilibili_bgmcount": epi,
        "bilibili_season": season,
    }