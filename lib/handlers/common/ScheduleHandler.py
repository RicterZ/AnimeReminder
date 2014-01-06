# -*- coding:utf-8 -*-
from lib.anime import AnimeDataGetter
from lib.error import *
from lib.settings import *

class ScheduleGetHandler():
    weekDict = {
        '0': 'SUN',
        '1': 'MON',
        '2': 'TUE',
        '3': 'WED',
        '4': 'THU',
        '5': 'FRI',
        '6': 'SAT',
    }

    def GET(self):
        """说明：这个渣渣正则我回头再写好了=-="""
        web.header('Content-type', "application/json; charset=utf-8")
        anime = AnimeDataGetter()
        url = 'http://anime.kankan.com/'
        reqdata = anime.getURL(url)
        animelist, todaylist = [], []
        try:
            updatelist = re.compile(r'<li>\d\d:\d\d.*<a.*')
            updatetime = re.compile(r'<ul id="sche_show_\d">')
            time = re.compile(r'\d\d:\d\d')
            href = re.compile(r'http://.*\d\d\d\d\d')
            name = re.compile(r'">.*</a>')
            for i in reqdata.split('\n'):
                if updatetime.findall(i):
                    weekday = updatetime.findall(i)[0].split('"')[1].split('_')[2]
                if updatelist.findall(i):
                    data = updatelist.findall(i)[0].decode('utf8')
                    animelist.append({
                        "week": weekday,
                        "time": time.findall(data)[0],
                        "url": href.findall(data)[0],
                        "name": name.findall(data)[0].strip('">').split('<')[0]
                    })
        except:
            return returnData(500, ScheduleErrorMessage)
        else:
            return returnData(data={"update_list": animelist})