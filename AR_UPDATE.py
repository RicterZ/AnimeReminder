# -*- coding:utf-8 -*-

from lib.anime import AnimeDataGetter
import web, os
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

urls=(
    '/allupdate', 'allupdate'
)

db = web.database(host='ricter.info', dbn='mysql', db='ricter_newanime', user='ricter', pw='CanyueROOTSmile')

class allupdate:
    def GET(self):
        """
            全部更新
        """
        templatepath = '/home/ricter/web/anime/lib/emailtemp/'
        openheader = open(templatepath + "header", "r").read()
        openfooter = open(templatepath + "footer", "r").read()

        update = AnimeDataGetter()
        data = db.query('select * from anmielist where isover=0 order by id')
        """data = db.query('select * from anmielist where 1')
        for anime in data:
            animeData = update.getDetail(str(int(anime.animeid)))
            print '** ' + anime.animename
            db.update('anmielist', where = 'animeid=' + anime.animeid, \
                poster = update.AnimePoster, detail = update.AnimeIntro)
            update.__init__()"""

        isnew = db.query('select * from anmielist where isnew > 0')
        for anime in isnew :
            isnewnum = anime.isnew - 1
            db.update('anmielist', where="animeid=" + anime.animeid, isnew = isnewnum)

        
			
        newanimelist = []
        for anime in data:
            print '** ' + anime.animename
            isSuccess = update.getDetail(anime.animeid)
            if isSuccess:
                if not str(update.AnimeEpiCount) == str(anime.episode):
                    db.delete('anmielist', where="id=" + str(anime.id))
                    db.insert('anmielist', animeid = anime.animeid, animename = anime.animename, \
                              episode = update.AnimeEpiCount, isnew = 12, isover = update.AnimeIsOver)
                    newanimelist.append(anime.animeid)

        if newanimelist:
            updateusers = db.query("select * from user where animelist != ''")
            for user in updateusers:
                sendbody = ''
                useranimelist = user.animelist.split('|')[:-1]
                readlist = list(str(user.isread))
                isupdate = False
                for anime in useranimelist:
                    if anime in newanimelist:
                        isupdate = True
                        t = db.query('select * from anmielist where animeid=' + anime)[0]
                        sendbody = sendbody + \
                        '<table class="w580" width="580" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td class="w580" width="580">' + \
                        '<p align="left" class="article-title"><a href="http://data.movie.kankan.com/movie/' + \
                        str(anime) + '">' + t.animename + '</a><span class="cs-el-wrap">更新到第 ' + str(t.episode) \
                        + ' 集</span></p><br /></tbody></table>'

                        readlist[useranimelist.index(anime)] = '1'


                if isupdate:
                    #print ''.join(readlist)
                    db.update('user', where="uid=" + user.uid, isread = ''.join(readlist))
                    if str(user.isremind) == '1':
                        print '** ' + user.email
                        web.sendmail(
                            'Anime Reminder', 
                            user.email, 
                            '新番提醒，您的以下订阅有更新', 
                            openheader + sendbody + openfooter, 
                            headers={'Content-Type':'text/html;charset=utf-8','User-Agent': 'webpy.sendmail', 'X-Mailer': 'webpy.sendmail'}
                        )

        return 0

app = web.application(urls, globals())
if __name__ == "__main__":app.run()
#application = web.application(urls, globals()).wsgifunc()
