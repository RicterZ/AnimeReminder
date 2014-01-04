from lib.handlers.common.BaseHandler import WebBaseHandler
from lib.settings import *

class GetUserInfoHandler(WebBaseHandler):
    def GET(self):
        if not self.isLogin: return returnData(500, KeyErrorMessage)
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
            "unread": int(self.updateNum)
        })


class EmailStatusSetHandler(WebBaseHandler):
    def GET(self):
        if not self.isLogin: return returnData(500, KeyErrorMessage)
        enable = web.input(enable='0').enable
        if not enable == '1':enable = '0'
        db.update('user', where="id=%d"%self.uid, isremind=enable)

        return returnData()