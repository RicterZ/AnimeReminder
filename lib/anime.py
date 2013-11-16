# -*- coding:utf-8 -*-
import urllib2
import json
import re

class AnimeDataGetter(object):
    _searchUrl  = 'http://mediaso.xmp.kankan.xunlei.com/search.php?keyword='
    #_searchUrl  = 'http://search.pad.kankan.com/search4phone.php?keyword='
    _detailUrl  = 'http://data.pad.kankan.com/mobile/detail/'
    _sub_detailUrl = 'http://data.pad.kankan.com/mobile/sub_detail/'

    def getURL(self, url):
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req)
        return resp.read()

    def animeSearch(self, amimeName):
        return self.__getAnimeSearchList__(self.getURL(self._searchUrl + amimeName))

    def __getAnimeSearchList__(self, data):
        data, searchList = data.split('\n'), []
        del data[:2];del data[-2:]
        sname = re.compile(r'sname=".+?"');imovieid = re.compile(r'imovieid=\d*')
        for i in data:
            if sname.findall(i) and imovieid.findall(i):
                searchList.append([sname.findall(i)[0].split('=')[1].strip('"'), imovieid.findall(i)[0].split('=')[1]])
        return searchList

    def getDetail(self, id):
        try:
            detailData = self.getURL(self._detailUrl + id[:2] + '/' + id + '.json')
            detailDic = json.loads(detailData)
            self.AnimeAid         = detailDic['id']
            self.AnimeTitle       = detailDic['title']
            self.AnimePoster      = detailDic['poster']
            self.AnimeIntro       = detailDic['intro']
            self.AnimeEpiCount    = detailDic['episodeCount']
            self.AnimeDisplayType = detailDic['displayType']
            if 'totalEpisodeCount' in detailDic.keys():
                self.AnimeIsOver      = '1';
            else:
                self.AnimeIsOver      = '0';
            return True
        except:
            return False


#DEMO
#----------------------------------------------------------
"""
anime = AnimeDataGetter()
print anime.animeSearch('悠哉日常大王')
if anime.getDetail('74030'):
    print 'id:', anime.AnimeAid
    print 'title:', anime.AnimeTitle
    print 'poster:', anime.AnimePoster
    print 'intro:', anime.AnimeIntro
    print 'episodeCount:', anime.AnimeEpiCount
    print 'isover:', anime.AnimeIsOver
"""
#----------------------------------------------------------
