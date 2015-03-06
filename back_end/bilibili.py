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


def parse_episode(sp_id, season_id=0):
    # TODO: 有可能会有中文集数，或者第⑨集这样的
    match_epi = re.compile('<div class="t">第(\d+)-?(\d+)?集</div>')
    param = str(sp_id) if not season_id else '%d-%d' % (sp_id, season_id)
    bangumi_url = 'http://www.bilibili.tv/sppage/bangumi-%s-1.html' % param
    response = urllib2.urlopen(bangumi_url).read()

    result = match_epi.findall(response)
    return 0 if not result else int(result[0][0]) if not result[0][1] else int(result[0][1])


def get_real_name(name):
    url = urllib2.urlopen('http://www.bilibili.tv/sp/%s' % name).url
    name = url.split('/')[-1]
    return name if not name.startswith('search') else None


def get_anime_detail(name):
    api_url = 'http://api.bilibili.tv/sp?title=%s'
    real_title = get_real_name(name)

    # the anime not exist on the bilibili
    if not real_title:
        return {}

    sp_data = json.loads(urllib2.urlopen(api_url % real_title).read())
    season, season_id = 0, 0

    sp_id = sp_data['spid']
    if 'season' in sp_data:
        for index in sp_data['season']:
            season_data = sp_data['season'][index]
            if season_data['default']:
                season = parse_season(season_data['season_name'])
                season_id = season_data['season_id']
                break
    season = int(season) if season else 1
    episode = parse_episode(sp_id, season_id)

    return {
        "aid": sp_id,
        "link": "http://www.bilibili.tv/sp/%s" % real_title,
        "episode": episode,
        "season": season,
        "name": urllib2.unquote(real_title),
    }


if __name__ == '__main__':
    print get_real_name('asdad')