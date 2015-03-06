#coding:utf-8
import requests
from datetime import datetime


BILI_URL = 'http://www.bilibili.com/'
BILI_API_URL = 'http://api.bilibili.com/'


def parse_episode(sp_id, season_id=0):
    '''获取每一季的番剧集数'''
    # TODO: 对于合集的处理
    bangumi_url = BILI_API_URL + 'spview'
    params = {
        'spid': sp_id,
        'bangumi': 1,
        'season_id': season_id,
    }

    try:
        response = requests.get(bangumi_url, params=params).json()
    except requests.RequestException:
        # -1 表示获取失败，需要人工重新获取
        return -1

    return response['count']


def parse_season(aid, seasons):
    '''处理每一季的数据'''
    return [{
        'season_id': season['season_id'],
        'name': season['season_name'],
        'default': season['default'],
        'cover': season['index_cover'],
        'count': parse_episode(aid, season['season_id'])
    } for season in seasons]


def get_real_name(name):
    '''获取番剧的通用名称'''
    # TODO: 需要修改
    url = requests.get(BILI_URL + 'sp/%s' % name).url
    name = url.split('/')[-1]
    return name if not name.startswith('search') else None


def get_anime_detail(name):
    '''获取番剧详情'''
    api_url = BILI_API_URL + 'sp?title=%s'
    real_title = get_real_name(name)

    # the anime not exist on the bilibili
    if not real_title:
        return {}


    bangumi_data = requests.get(api_url % real_title).json()
    season = parse_season(bangumi_data['spid'], bangumi_data['season']) if 'season' in bangumi_data else {}
    episode = sum((i['count'] for i in season)) if season else parse_episode(bangumi_data['spid'])

    return {
        'aid': bangumi_data['spid'],
        'episode': episode,
        'season': season,
        'is_end': bangumi_data['isbangumi_end'],
        'name': bangumi_data['title'],
        'cover': bangumi_data['cover'],
        'description': bangumi_data['description'],
        'link': BILI_URL + 'sp/%s' % real_title,
        'lastupdate': bangumi_data['lastupdate']
    }


def search(name):
    url = BILI_API_URL + 'search/'
    params = {'keyword': name}

    try:
        result = requests.get(url, params=params).json()
    except ValueError:
        return {}
    return convert_to_response(result)


def convert_to_response(result):
    return [{
        'aid': row['spid'],
        'name': row['title'],
        'description': row['description'],
        'episode': row['count'],
        'poster_link': row['pic'],
        'updated_time': datetime.fromtimestamp(row['lastupdate']),
    } for row in result['result'] if 'spid' in row]

