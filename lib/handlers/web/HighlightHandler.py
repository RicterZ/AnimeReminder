from lib.handlers.common.BaseHandler import WebBaseHandler
from lib.settings import *

class HighLightHandler(WebBaseHandler):
    def GET(self):
        if not self.isLogin: return returnData(KeyErrorMessage)
        webinput = web.input(aid='',method='add')
        try:
            animeid = str(int(webinput.aid))
        except:
            return returnData(UnknowErrorMessage)
        method = '1' if webinput.method == 'add' else '0'
        if not animeid in self.animelist or not animeid: return returnData(AnimeErrorMessage)
        self.isread[self.animelist.index(animeid)] = method
        db.update('user', where="id=%d"%self.uid, isread = ''.join(self.isread))
        return returnData()
