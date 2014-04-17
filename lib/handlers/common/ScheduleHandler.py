# -*- coding:utf-8 -*-
from lib.settings import *


class ScheduleGetHandler(object):
    def GET(self):
        web.header('Content-type', "application/json; charset=utf-8")
        anime_list = db.select('schedule', where='id=2')[0]
        return returnData(data={"update_list": json.loads(anime_list.raw_data)})


class ScheduleGetHandlerV2(object):
    def GET(self):
        web.header('Content-type', "application/json; charset=utf-8")
        anime_list = db.select('schedule', where='id=1')[0]
        return returnData(data={"update_list": json.loads(anime_list.raw_data)})