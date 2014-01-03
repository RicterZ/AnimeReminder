from lib.handlers.BaseHandler import WebBaseHandler
from lib.settings import *

class SearchHandler(WebBaseHandler):
    def GET(self):
        render = web.template.render('templates')
        return render.search()

    def POST(self):
        keyword = web.input(keyword='').keyword
        if keyword:
            s = AnimeDataGetter()
            return returnData(
                data=[{
                    'aid': animeItem[1],
                    'name': animeItem[0].decode('utf-8'),
                } for animeItem in s.animeSearch(keyword.encode('gbk'))]
            )
        else:
            return returnData(500, DataErrorMessage)