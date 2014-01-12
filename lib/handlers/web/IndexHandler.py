# -*- coding:utf-8 -*-
from lib.handlers.common.BaseHandler import WebBaseHandler
from lib.settings import *

class IndexDataHandler(WebBaseHandler): 
    def GET(self):
        data = db.query('select * from anmielist where 1 order by id desc limit 0,8')
        animeList = [{
            "name"   : i.animename,
            "animeid": i.animeid, 
            "episode": int(i.episode), 
            "isnewer": int(i.isnew),
            "isover" : int(i.isover),
        } for i in data]

        return json.dumps({
            "status": 200,
            "message": "",
            "data": animeList
        })
