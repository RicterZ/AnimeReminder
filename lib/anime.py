# -*- coding:utf-8 -*-
import urllib2
import json
import re
import zipfile
import os

class AnimeDataGetter(object):
    AnimeAid      = ''
    _searchUrl    = 'http://mediaso.xmp.kankan.xunlei.com/search.php?keyword='
    _detailUrl    = 'http://data.pad.kankan.com/mobile/detail/'
    _subDetailUrl = 'http://data.pad.kankan.com/mobile/sub_detail/'
    _listUrl      = 'http://pianku.xmp.kankan.com/movielua/'
    fuckList = ['60773', '74299']
    sname = re.compile(r'sname=".+?"')
    imovieid = re.compile(r'imovieid=\d*')

    def __init__(self):
       self.AnimeTitle    = ''
       self.AnimePoster   = ''
       self.AnimeIntro    = ''
       self.AnimeEpiCount = ''
       self.AnimeIsOver   = '0'

    def getURL(self, url):
        """
            传入URL，"http://"这玩意一定要有
            访问URL获取Data并Return
            貌似没有容错，也就这么着吧..
        """
        return urllib2.urlopen(urllib2.Request(url)).read()

    def animeSearch(self, amimeName):
        return self.__getAnimeSearchList__(self.getURL(self._searchUrl + amimeName))

    def __getAnimeSearchList__(self, data):
        """
            处理搜索得到的数据，渣渣正则
            返回一个二级列表，内容是[['名称1', 'id1'], ['名称2', 'id2']]
        """
        data, searchList = data.split('\n'), []
        del data[:2];del data[-2:]
        for i in data:
            if self.sname.findall(i) and self.imovieid.findall(i):
                searchList.append([self.sname.findall(i)[0].split('=')[1].strip('"'), \
                self.imovieid.findall(i)[0].split('=')[1]])
        return searchList

    def getDetail(self, id):
        if id in self.fuckList:return self.getDetailByLua(id)
        try:
            detailData = self.getURL(self._detailUrl + id[:2] + '/' + id + '.json')
            detailDic = json.loads(detailData)
            self.AnimeAid      = detailDic['id']
            self.AnimeTitle    = detailDic['title']
            self.AnimePoster   = detailDic['poster']
            self.AnimeIntro    = detailDic['intro']
            self.AnimeEpiCount = detailDic['episodeCount']
            if 'totalEpisodeCount' in detailDic.keys():
                self.AnimeIsOver  = '1';
            return True
        except Exception, e:
            return self.getDetailByLua(id)

    def getDetailByLua(self, id):
        try:
            with open(id + ".zip", "wb") as code:
                listdata = self.getURL(self._listUrl + id[:2] + '/' + id + '.lua.zip')
                code.write(listdata)
            zfile = zipfile.ZipFile(id + ".zip", 'r')
            file = open(id + '.lua', 'w+b');
            file.write(zfile.read(id + '.lua'))
            file.close();zfile.close()
        except Exception, e:
            print e
            os.remove(id + '.zip') 
            return False
        else:
            openfile = open(id + '.lua', 'r')
            subMovie = re.compile(r'local subMovie = {.*}')
            subDetail = subMovie.findall(openfile.read())[0]
            icount = re.compile(r'icount = \d*')
            imovieid = re.compile(r'imovieid=\d*')
            isover = re.compile(r'ilastupdatesubmovieid=\d*')
            smoviename = re.compile(r'smoviename=".+?"')
            self.AnimeEpiCount = icount.findall(subDetail)[0].split("=")[1].strip(' ')
            self.AnimeAid      = imovieid.findall(subDetail)[0].split("=")[1]
            self.AnimeTitle    = smoviename.findall(subDetail)[0].decode('utf-8').split("=")[1].strip('"')
            if isover.findall(subDetail)[0].split("=")[1] == '0':
                self.AnimeIsOver = '1'
            openfile.close()
            os.remove(id + '.lua')
            os.remove(id + '.zip') 
            return True



if __name__ == "__init__":
    anime = AnimeDataGetter()
    print anime.animeSearch('悠哉日常')
    if anime.getDetail('74022'):
        print 'id:', anime.AnimeAid
        print 'title:', anime.AnimeTitle
        print 'poster:', anime.AnimePoster
        print 'intro:', anime.AnimeIntro
        print 'episodeCount:', anime.AnimeEpiCount
        print 'isover:', anime.AnimeIsOver
    anime.__init__()
    if anime.getDetailByLua('74022'):
        print 'id:', anime.AnimeAid
        print 'title:', anime.AnimeTitle
        print 'poster:', anime.AnimePoster
        print 'intro:', anime.AnimeIntro
        print 'episodeCount:', anime.AnimeEpiCount
        print 'isover:', anime.AnimeIsOver