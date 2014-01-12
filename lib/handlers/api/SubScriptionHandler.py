from lib.handlers.common.BaseHandler import APIBaseHandler
from lib.settings import *

class AddAnimeHandler(APIBaseHandler):
    def GET(self):
        if not self.isKey: return returnData(KeyErrorMessage)
        try:
            animeid = str(int(web.input(aid='').aid))
        except:
            return returnData(UnknowErrorMessage)
        if not animeid: return returnData(AnimeNotExistMessage)
        data = db.select('anmielist', where='animeid="%s"'%animeid)

        if len(data) == 0:
            anime = AnimeDataGetter()
            isSuccess = anime.getDetail(animeid)
            if not isSuccess: return returnData(AnimeNotExistMessage)
            db.insert('anmielist', animename = anime.AnimeTitle, \
                animeid = anime.AnimeAid, episode = anime.AnimeEpiCount,\
                isover = anime.AnimeIsOver, poster = anime.AnimePoster, \
                detail = anime.AnimeIntro)

        if animeid in self.animelist: return returnData(AddRepateMessage)
        db.update('user', where='id=%d'%self.id, animelist=animeid + '|' + \
        self.animestr, isread='0'+str(self.isreadstr), epilook = '0|' + self.epistr)
        return returnData()

class DelAnimeHandler(APIBaseHandler):
    def GET(self):
        if not self.isKey: return returnData(KeyErrorMessage)
        try:
            animeid = str(int(web.input(aid='').aid))
        except:
            return returnData(UnknowErrorMessage)
        if not animeid: return returnData(AnimeNotExistMessage)

        try:
            epilook2 = ''
            self.epilook[self.animelist.index(animeid)] = ''
            for i in self.epilook:
                if i and epilook2:epilook2 = epilook2 + '|' + i
                if i and not epilook2:epilook2 = i
        except:
            epilook2 = '|'.join(self.epilook)

        if not animeid in self.animelist: return returnData(AnimeErrorMessage)
        self.isread[self.animelist.index(animeid)] = ''
        animeliststr = self.animestr.replace(animeid + '|', '')
        if epilook2:
            db.update('user', where="id=%d"%self.id, animelist = animeliststr, \
            isread = ''.join(self.isread), epilook = epilook2 + '|')
        else:
            db.update('user', where="id=%d"%self.id, animelist = animeliststr, \
            isread = ''.join(self.isread), epilook = epilook2)
        return returnData()


class EpiEditHandler(APIBaseHandler):
    def GET(self):
        if not self.isKey: return returnData(KeyErrorMessage)
        webinput = web.input(aid='',epi='0')
        try: 
            animeid = str(int(webinput.aid))
            epinum = str(int(webinput.epi))
        except:
            return returnData(UnknowErrorMessage)
        if not epinum or not animeid: return returnData(UnknowErrorMessage)
        episode = db.select('anmielist',what='episode',where='animeid=%s'%animeid)
        if not episode: return returnData(AnimeNotExistMessage)
        episode = episode[0].episode

        if not animeid in self.animelist: return returnData(AnimeErrorMessage)
        if int(episode) < int(epinum): return returnData(EpisodeErrorMessage)

        self.epilook[self.animelist.index(animeid)] = epinum
        db.update('user',where="id=%d"%self.id,epilook='|'.join(self.epilook)+'|')
        return returnData()