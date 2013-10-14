# -*- coding:utf-8 -*-

from lib.anime import new_anime
import web, os
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

os.chdir('animelua')
urls=(
    '/allupdate', 'allupdate',
)

global db
db = web.database(dbn='mysql', db='', user='', pw='')

class allupdate:
    def GET(self):
        """
            全部更新
        """
        openheader = open("lib/emailtemp/header", "r").read()
        openfooter = open("lib/emailtemp/footer", "r").read()
        sendbody = ''

        update = new_anime()
        data = db.query('select * from anmielist where isover=0 order by id')

        isnew = db.query('select * from anmielist where isnew > 0')
        for anime in isnew :
            isnewnum = anime.isnew - 1
            db.update('anmielist', where="animeid=" + anime.animeid, isnew = isnewnum)

        newanimelist = []
        for anime in data:
            print '** ' + anime.animename
            episode = update.getNewEpisode(anime.animeid, True)
            if not isinstance(episode, int):
                if not str(episode[0]) == str(anime.episode):
                    db.delete('anmielist', where="id=" + str(anime.id))
                    db.insert('anmielist', animeid = anime.animeid, animename = anime.animename, \
                              episode = episode[0], isnew = 12, isover = episode[1])
                    newanimelist.append(anime.animeid)

        if newanimelist:
            updateusers = db.query('select * from user where 1')
            for user in updateusers:
                if not user.animelist == '':
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
                            str(anime) + '">' + t.animename + '</a><span class="cs-el-wrap">更新到第 ' + str(t.episode) + ' 集</span></p><br />'

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
		
application = web.application(urls, globals()).wsgifunc()
