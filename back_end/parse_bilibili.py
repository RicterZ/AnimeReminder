#coding:utf-8

import urllib2

"""
这里的都是解析bilibili各种API的函数
"""

def parse_epi(sp_id, season_id=0):
    
    param = str(sp_id)
    if season_id:
    	param += '-' + str(season_id)

    request_url = 'http://www.bilibili.tv/sppage/bangumi-%s-1.html' % param

    result = urllib2.urlopen(request_url).read()
    begin  = result.find('<div class="t">')
    end    = result.find('</div></a>')

    if begin == -1 or end == -1:
    	return 0

    return int(result[begin+18 : end-3])

