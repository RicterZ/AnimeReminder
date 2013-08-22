# -*- coding:utf-8 -*-
import urllib,urllib2
import re, os
import zipfile

class new_anime(object):
    """
        新番动漫提醒类
        迅雷看看不公布api，我自己抓了几个包
    """
    _searchUrl  = 'http://mediaso.xmp.kankan.xunlei.com/search.php?keyword='
    _listUrl    = 'http://pianku.xmp.kankan.com/movielua/'
    _listExName = '.lua.zip'
    _ml         = '/home/ricter/web/anime/animelua/'

    def getURL(self, url):
        """
            获取URL返回的内容
        """
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req)
        return resp.read()

    def animeSearch(self, amimeName):
        """
            根据名称搜索动漫，调用getAnimeSearchList返回搜索到的列表
        """
        return self.__getAnimeSearchList__(self.getURL(self._searchUrl + amimeName))

    def __getAnimeSearchList__(self, data):
        """
            传入搜索到的文本
            解析文本，获取搜索到的动漫名称以及imovieid
            这里用正则表达式，没啥技术含量
            返回一个LIst，需要自己判断是否为空
        """
        data, searchList = data.split('\n'), []
        del data[:2];del data[-2:]
        sname = re.compile(r'sname=".+?"');imovieid = re.compile(r'imovieid=\d*')
        for i in data:
            if sname.findall(i) and imovieid.findall(i):
                searchList.append([sname.findall(i)[0].split('=')[1].strip('"'), imovieid.findall(i)[0].split('=')[1]])
        return searchList

    def getNewEpisode(self, id, reupdate = False):
        """
            获取最新集数，返回一个数字
            若返回数字大于0，则证明存在动漫
            若返回数字等于0，则证明不存在动漫
            若返回数字等于-1，则证明搜索过程出错或者下载过程出错
        """
        epilist = []
        os.chdir(self._ml)
        if reupdate:
            if self.__getAnimeList__(id, True) == -1:
                return -1
        else:
            if self.__getAnimeList__(id) == -1:
                return -1
        openfile = open(id + '.lua', 'r')
        sname = re.compile(r'sname=".+?"')
        os.chdir('..')
        for line in openfile.read().split('\n'):
            if sname.findall(line):
                try: 
                    epilist.append(int(sname.findall(line)[0].split('=')[1].decode("utf8")\
                          .strip('"').replace(u'第', '').replace(u'集', '')))
                except:
                    return 0
        if epilist:
            temp = 0
            for i in epilist:
                if i > temp:
                    temp = i
            return temp
        return 0

    def getNameByID(self, id):
        """
            根据ID获取动漫名称
        """
        os.chdir(self._ml)
        if self.__getAnimeList__(id) == -1:
            return ''
        openfile = open(id + '.lua', 'r')
        os.chdir('..')
        smoviename = re.compile(r'smoviename=".+?"')
        for line in openfile.read().split('\n'):
            if smoviename.findall(line):
                try: 
                    return smoviename.findall(line)[0].split('=')[1].decode("utf8")
                except:
                    return ''
                break
        return ''
		
        

    def __getAnimeList__(self, id, reupdate = False):
        """
            获取动漫集数列表，返回一个列表
            -------------------------------
            这里很蛋疼..
            动漫列表在一个zip压缩包里面，需要下载下来，解压，获取..
            难道迅雷看看就是这样运作的么..
        """
        #try:
        #    os.remove(id + '.zip')
        #except:
        #    print 'None'

        try:
            if reupdate:
                with open(id + ".zip", "wb") as code:
                    listdata = self.getURL(self._listUrl + id[:2] + '/' + id + self._listExName)
                    code.write(listdata)

            if not os.path.exists(id + ".lua"):      #不存在列表文件则下载
                if not os.path.exists(id + ".zip"): 
                     with open(id + ".zip", "wb") as code:
                        listdata = self.getURL(self._listUrl + id[:2] + '/' + id + self._listExName)
                        code.write(listdata)

            zfile = zipfile.ZipFile(id + ".zip",'r')
            filename = id + '.lua'
            data = zfile.read(filename)
            file = open(filename, 'w+b');file.write(data)
            file.close();zfile.close()
            os.remove(id + '.zip')                #删除下载的zip文件
        except:
            return -1

#DEMO
#----------------------------------------------------------
xunlei = new_anime()
print xunlei.animeSearch('丧女')
