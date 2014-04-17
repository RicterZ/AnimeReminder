# -*- coding:utf-8 -*-
from lib.settings import *


class ScheduleGetHandler(object):
    def GET(self):
        web.header('Content-type', "application/json; charset=utf-8")
        anime_list = db.select('schedule', where='id=2')
        return returnData(data={"update_list": json.loads(anime_list)})


class ScheduleGetHandlerV2(object):
    def GET(self):
        web.header('Content-type', "application/json; charset=utf-8")
        anime_list = db.select('schedule', where='id=1')
        return returnData(data={"update_list": json.loads(anime_list)})