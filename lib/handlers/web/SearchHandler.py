# -*- coding:utf-8 -*-
from lib.handlers.common.BaseHandler import WebBaseHandler
from lib.settings import *

class SearchHandler(WebBaseHandler):
    def GET(self):
        web.header('Content-type', "text/html; charset=utf-8")
        return self.render('search.html', title = '搜索'.decode('utf-8'))

    def POST(self):
        keyword = web.input(keyword='').keyword
        if keyword:
            s = AnimeDataGetter()
            return returnData(
                data=[{
                    'id': animeItem[1],
                    'name': animeItem[0].decode('utf-8'),
                } for animeItem in s.animeSearch(keyword.encode('gbk'))]
            )
        else:
            return returnData(500, DataErrorMessage)