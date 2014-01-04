# -*- coding:utf-8 -*-
from lib.handlers.common.BaseHandler import WebBaseHandler
from lib.settings import *

class IndexPage(WebBaseHandler):
    def GET(self):
        web.header('Content-type', "text/html; charset=utf-8")
        return self.render('index.html', title = '主页'.decode('utf-8'))


class UserPage(WebBaseHandler):
    def GET(self):
        web.header('Content-type', "text/html; charset=utf-8")
        return self.render('my.html', title = '我'.decode('utf-8'))

class AnimeHandler(WebBaseHandler):
    def GET(self, aid):
        import urllib2
        web.header('Content-type', "text/html; charset=utf-8")
        req = urllib2.urlopen('http://data.pad.kankan.com/mobile/detail/%s/%s.json' % (str(aid)[:2], aid))
        try:
            data = json.loads(req.read())
        except:
            data = db.select('anmielist', where='animeid=%s'%aid)
            if data:
                data = data[0]
                data = {
                    'title': data.animename,
                    'id': data.animeid,
                    'poster': data.poster,
                    'intro': data.detail,
                }
            else:
                return web.seeother('/')

        return self.render('detail.html',title=data['title'],data=data)