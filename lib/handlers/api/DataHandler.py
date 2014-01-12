from lib.handlers.common.BaseHandler import APIBaseHandler
from lib.settings import *

class GetUserInfoHandler(APIBaseHandler):
    def GET(self):
        if not self.isKey: return returnData(KeyErrorMessage)
        dataList = []
        for i in range(0, len(self.animelist)):
            animeData = db.select(
                'anmielist',what="animename,episode,isover",\
                where="animeid=" + self.animelist[i]
            )[0]
            dataList.append({
                "id": int(self.animelist[i]),
                "name": animeData.animename,
                "isover": int(animeData.isover),
                "episode": int(animeData.episode),
                "watch": int(self.epilook[i]),
                "isread": int(self.isread[i]),
            })
        return returnData(data={
            "subscription": dataList,
            "email": int(self.isremind),
        })


class EmailStatusSetHandler(APIBaseHandler):
    def GET(self):
        if not self.isKey: return returnData(KeyErrorMessage)
        enable = web.input(enable='0').enable
        if not enable == '1':enable = '0'
        db.update('user', where="id=%d"%self.id, isremind=enable)

        return returnData()

