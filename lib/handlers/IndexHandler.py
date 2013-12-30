# -*- coding:utf-8 -*-
from lib.handlers.BaseHandler import WebBaseHandler
from lib.settings import *

class gotoIndex:
    def GET(self):
        return web.seeother('/index.html')

class IndexHandler(WebBaseHandler): 
    def GET(self):
        data = db.query('select * from anmielist where 1 order by id desc limit 0,8')
        animeList = [{
            "name"   : i.animename,
            "animeid": i.animeid, 
            "episode": int(i.episode), 
            "isnewer": int(i.isnew),
            "isover" : int(i.isover),
            #"intro"  : i.detail,
        } for i in data]

        return json.dumps({
            "status": 200,
            "message": "",
            "data": animeList
        })
        #return self.render('animeList.html', '动漫更新表'.decode('utf8'), animeList = animeList, \
        #isLogin = self.isLogin, uid = self.uid, newnum = self.updateNum)


class SearchHandler(WebBaseHandler):
    def GET(self):
        anime = AnimeDataGetter()
        animename = web.input(n='').n 
        if animename:
            return self.render(
                'search.html', "搜索结果".decode('utf8'),
                searchResultList = anime.animeSearch(animename.encode('gbk')),
                isLogin = self.isLogin, 
                newnum = self.updateNum
            ) 
        else:
            return web.seeother('/')