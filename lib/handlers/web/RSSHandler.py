__author__ = 'Ricter'
from lib.handlers.common.BaseHandler import WebBaseHandler
from lib.settings import *


class RSSHandler():
    def __init__(self):
        pass

    def GET(self, user_id):
        web.header('Content-type', "text/xml; charset=utf-8")
        data_list = []
        anime_list = db.select('user', where="id=%d" % int(user_id))[0]
        for i in anime_list.animelist.split('|')[:-1]:
            anime_data = db.select(
                'anmielist',what="animename,episode",
                where="animeid=%d" % int(i)
            )[0]
            data_list.append({
                "id": int(i),
                "name": anime_data.animename,
                "episode": int(anime_data.episode),
            })
        return env.get_template("rss.xml").render(data=data_list)