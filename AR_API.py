# -*- coding:utf-8 -*-
#-----------------------------------------------
#Anime Update alert
#E-mail:canyuexiaolang@gmail.com
#Website:http://www.ricter.info
#-----------------------------------------------


from lib.anime import AnimeDataGetter
import urllib,urllib2
import re, os
import zipfile, datetime
import web
import random, hashlib, string

web.config.debug = False

urls=(
    '/login', 'LoginHandler',
    '/reg', 'RegHandler',
    '/get_subscription_list', 'GetSubscriptionHandler',
    '/email_reminder_get', 'EmailStatusGetHandler',
    '/email_reminder_set', 'EmailStatusSetHandler',
    '/get_update_schedule', 'ScheduleGetHandler',
    '/del_highlight', 'DelAnimeHighLightHandler',
    '/add_highlight', 'AddAnimeHighLightHandler',
    '/epiedit', 'LookToEpiEditHandler',
    '/changepw', 'ChangePasswordHandler',
    '/add_anime', 'AddAnimeHandler',
    '/del_anime', 'DelAnimeHandler'
)

dbhost  = '127.0.0.1'             #数据库地址
dbtype  = 'mysql'                 #数据库类型
dbname  = ''                      #数据库名
dbun    = ''                      #数据库用户名
dbpw    = ''                      #数据库密码
tempdir = '../templates'          #模板目录设置

global db
global render
db = web.database(host=dbhost, dbn=dbtype, db=dbname, user=dbun, pw=dbpw)
render = web.template.render(os.path.abspath(os.path.dirname('/home/ricter/web/anime/ricter')) + '/templates/', cache=True)
web.config.debug = False                                                         #关闭调试模式

class BaseHandler:
    key = ''
    iskey = True
    iskeyerror = False
    isPlug = False

    def __init__(self):
        web.header('Content-type', "text/html; charset=utf-8")
        try:
            self.key = web.input().key.replace("'", '').replace('"', '')\
                  .replace('\\', '').replace('/', '').replace('?', '')\
                  .replace(' ', '')
        except:
            self.iskey = False

        if self.returnUA(web.ctx.env.get('HTTP_USER_AGENT')) == 'Plugin':
            self.isPlug = True

        if self.iskey:
            try: 
                if self.isPlug:
                    print "** Plug"
                    user_data = db.query('select * from user where keyid_plug="' + self.key + '"')[0]
                else:
                    print "** App"
                    user_data = db.query('select * from user where keyid="' + self.key + '"')[0]
            except:
                self.iskeyerror = True
            else:
                self.uid = user_data.uid
                self.animestr = user_data.animelist
                self.epistr = user_data.epilook
                self.password = user_data.password
                self.animelist = user_data.animelist.split('|')[:-1]
                self.epilook = user_data.epilook.split('|')[:-1]
                self.isread = list(user_data.isread)
                self.isreadstr = user_data.isread
                self.isremind = user_data.isremind

    def pwToMD5(self, pwstr):
        h = hashlib.md5()
        h.update(pwstr)
        return h.hexdigest()

    def getEmailReminderStatus(self):
        return self.isremind

    def returnUA(self, userAgent):
        userAgentList = userAgent.split(".")
        #print userAgentList
        if not userAgentList[0] == 'AnimeReminder':
            try:
                if int(web.input().ua) == 1:return 'Plugin'
            except:
                return 'Browser'
        if userAgentList[1] == 'Mobile':return 'Mobile'
        return 'Browser'

        
class RegHandler(BaseHandler):
    def GET(self):
        try:
            email = web.input().u.replace(' ', '')\
            .replace('"', '').replace("'", '')\
            .replace("<", '').replace(">", '')\
            .replace("\\", '').replace("/", '')
            password = self.pwToMD5(web.input().p)
        except:
            return 'ERROR_INVALID_DATA'

        if not '@' in email or not '.' in email:
            return 'ERROR_INVALID_DATA'
        if email.find('@') == -1 or len(email) > 50:
            return 'ERROR_INVALID_DATA'

        uid = str(random.randrange(1000000,9999999)) + str(random.randrange(1000000,9999999))

        #检查UID是否重复
        data = db.query('select uid from user where uid="' + uid + '"')
        while not len(data) == 0:
            uid = str(random.randrange(1000000,9999999)) + str(random.randrange(1000000,9999999))
            data = db.query('select uid from user where uid="' + uid + '"')
 
        #检查邮箱是否重复
        data = db.query('select uid from user where email="' + email + '"')
        if not len(data) == 0:
            return 'ERROR_EXIST_EMAIL'

        data = db.insert('user', email = email, password = password, emailid = '0', uid = uid)
        keyid = ''.join(random.sample(string.letters+string.digits, 10))
        if not self.isPlug:
            db.update('user', where="uid=" + uid, keyid = keyid)
        else:
            db.update('user', where="uid=" + uid, keyid_plug = keyid)
        return keyid

class LoginHandler(BaseHandler):
    def GET(self):
        try:
            username = web.input().u.replace(' ', '').replace('"', '')\
            .replace("'", '').replace("<", '').replace(">", '')\
            .replace("\\", '').replace("/", '')
            password = self.pwToMD5(web.input().p)
        except:
            return 'ERROR_INVALID_DATA'

        try:
            data = db.query('select * from user where email="' + username + '"')[0]
            psw = data.password
            if not psw == password:
                return 'ERROR_INVALID_PSW'
        except:
            return 'ERROR_INVALID_PSW'
        else:
            keyid = ''.join(random.sample(string.letters+string.digits, 10))
            if self.isPlug:
                db.update('user', where="email='" + username + "'", keyid_plug = keyid)
            else:
                db.update('user', where="email='" + username + "'", keyid = keyid)
            return keyid

class GetSubscriptionHandler(BaseHandler):
    def GET(self):
        try:
            ispull = str(web.input().sb)
        except:
            ispull = False
        else:
            ispull = True

        animedata_read, animedata_notread = [], []
        if self.iskey and not self.iskeyerror:
            for i in range(0, len(self.animelist)):
                data = db.select('anmielist', what="animename, episode, isover", where="animeid=" + self.animelist[i])[0]
                if self.isread[i] == '0':
                   animedata_read.append([self.animelist[i], data.animename, data.isover, data.episode, self.epilook[i], self.isread[i]])
                else:
                   animedata_notread.append([self.animelist[i], data.animename, data.isover, data.episode, self.epilook[i], self.isread[i]])
            if ispull:
                self.isreadstr = self.isreadstr.replace("1", "2")
                db.update('user', where="uid='" + self.uid + "'", isread = self.isreadstr)

            return render.api2('SUBLISTHANDLER', animedata_notread + animedata_read)
        else:
            return 'ERROR_INVALID_KEY'

class EmailStatusGetHandler(BaseHandler):
    def GET(self):
        if self.iskey and not self.iskeyerror:
            return self.getEmailReminderStatus()
        else:
            return 'ERROR_INVALID_KEY'

class EmailStatusSetHandler(BaseHandler):
    def GET(self):
        try:
            enable = str(int(web.input().enable))
            if not enable == '1':enable == '0'
        except:
            return 'ERROR_INVALID_DATA'

        if self.iskey and not self.iskeyerror:
            db.update('user', where="uid='" + self.uid + "'", isremind = enable)
            return 0
        else:
            return 'ERROR_INVALID_KEY'

class DelAnimeHighLightHandler(BaseHandler):
    def GET(self):
        if self.iskeyerror or not self.iskey:
            return 'ERROR_INVALID_KEY'

        ispulled = True
        try: #for Windows Phone 推送后的read状态
            temp = int(web.input().status)
        except:
            ispulled = False

        try:
            animeid = str(int(web.input().aid))
        except:
            return 'ERROR_INVALID_AID'

        if not animeid in self.animelist:

            return 'ERROR_INVALID_AID'

        if ispulled:
            self.isread[self.animelist.index(animeid)] = '2'
        else:
            self.isread[self.animelist.index(animeid)] = '0'

        db.update('user', where="uid='" + self.uid + "'", isread = ''.join(self.isread))
        return 0

class AddAnimeHighLightHandler(BaseHandler):
    def GET(self):
        if self.iskeyerror or not self.iskey:
            return 'ERROR_INVALID_KEY'

        ispulled = True
        try: #for Windows Phone 推送后的read状态
            temp = int(web.input().status)
        except:
            ispulled = False

        try:
            animeid = str(int(web.input().aid))
        except:
            return 'ERROR_INVALID_AID'

        if not animeid in self.animelist:
            return 'ERROR_INVALID_AID'
        else:
            if ispulled:
                self.isread[self.animelist.index(animeid)] = '2'
            else:
                self.isread[self.animelist.index(animeid)] = '1'

        db.update('user', where="uid='" + self.uid + "'", isread = ''.join(self.isread))
        return 0

class ScheduleGetHandler(BaseHandler):
    def GET(self):
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
                if updatetime.findall(i): weakday = updatetime.findall(i)[0].split('"')[1].split('_')[2]
                if updatelist.findall(i):
                    data = updatelist.findall(i)[0].decode('utf8')
                    anime = weakday + '|' + time.findall(data)[0] + '|' + href.findall(data)[0] + '|' + \
                    name.findall(data)[0].strip('">').split('<')[0]
                    animelist.append(anime)
            torrowlist, todaylist = [], []
            d = datetime.datetime.now()
            today = d.weekday() + 1
            torro = d.weekday() + 2
            if today == 7: today = 0
            if torro >= 7: torro = torro - 7
            for i in animelist:
                if i.split('|')[0] == str(today):
                    todaylist.append(i)
                if i.split('|')[0] == str(torro):
                    torrowlist.append(i)
        except Exception as e:
            return 'ERROR_GET_LIST: ' + str(e)
        else:
            return render.api2('SCHEDLUE', todaylist, torrowlist)

class ChangePasswordHandler(BaseHandler):
    def GET(self):
        if self.iskeyerror or not self.iskey:
            return 'ERROR_INVALID_KEY'

        try:
            oldpw = self.pwToMD5(web.input().oldpw)
            newpw = web.input().newpw
            if len(newpw) < 6 or len(newpw) > 16:
                return 'ERROR_INVALID_NEWPW'
            newpw = self.pwToMD5(newpw)
        except:
            return 'ERROR_INVALID_DATA'

        if not oldpw == self.password:
            return 'ERROR_INVALID_PSW'

        db.update('user', where="uid='" + self.uid + "'", password = newpw, keyid = '')
        return '0'

class LookToEpiEditHandler(BaseHandler):
    def GET(self):
        if self.iskeyerror or not self.iskey:
            return 'ERROR_INVALID_KEY'

        try:
            animeid = str(int(web.input().aid))
            epinum = str(int(web.input().epi))
            data = db.query('select * from anmielist where animeid="' + animeid + '"')
            episode = data[0].episode
        except:
            return 'ERROR_INVALID_DATA'

        if not animeid in self.animelist:return 'ERROR_INVALID_ANIME'
        if int(episode) < int(epinum):return 'ERROR_INVALID_EPI'
        try:
            self.epilook[self.animelist.index(animeid)] = epinum
            db.update('user', where="uid='" + self.uid + "'", epilook = '|'.join(self.epilook) + '|')
        except:
            return 'ERROR_SYSTEM'
        else:
            return '0'

class AddAnimeHandler(BaseHandler):
    def GET(self):
        if self.iskeyerror or not self.iskey:
            return 'ERROR_INVALID_KEY'

        try:
            animeid = str(int(web.input().aid))
        except:
            return 'ERROR_INVALID_AID'

        data = db.query('select * from anmielist where animeid="' + animeid + '"')
        if len(data) == 0:
            addData = False
        else:
            addData = True

        if addData:
            anime = AnimeDataGetter()
            isSuccess = anime.getDetail(animeid)
            if isSuccess:
                db.insert('anmielist', animename = anime.AnimeTitle, \
                    animeid = anime.AnimeAid, episode = anime.AnimeEpiCount,\
                    isover = anime.AnimeIsOver, poster = anime.AnimePoster, \
                    detail = anime.AnimeIntro)
            else:
                return 'ERROR_INVALID_AID'

        try: 
            if not animeid in self.animelist:
                db.update('user', where="uid='" + self.uid + "'", animelist = animeid + '|' + \
                self.animestr, isread = '0' + ''.join(self.isread), epilook = '0|' + self.epistr)
            else:
                return 'ERROR_EXIST_ANIME'
        except:
            return 'ERROR_SYSTEM'
        else:
            return '0'

class DelAnimeHandler(BaseHandler):
    def GET(self):
        if self.iskeyerror or not self.iskey:
            return 'ERROR_INVALID_KEY'

        try:
            animeid = str(int(web.input().aid))
        except:
            return 'ERROR_INVALID_AID'

        try:
            epilook2 = ''
            self.epilook[self.animelist.index(animeid)] = ''
            for i in self.epilook:
                if i and epilook2:epilook2 = epilook2 + '|' + i
                if i and not epilook2:epilook2 = i
        except:
            epilook2 = '|'.join(self.epilook)

        try:
            data = db.query('select * from anmielist where animeid="' + animeid + '"')
            if len(data) == 0:
                return 'ERROR_INVALID_AID'
            self.isread[self.animelist.index(animeid)] = ''
            animeliststr = self.animestr.replace(animeid + '|', '')
        except:
            return 'ERROR_SYSTEM'

        try:
            if epilook2:
                db.update('user', where="uid='" + self.uid + "'", animelist = animeliststr, \
                isread = ''.join(self.isread), epilook = epilook2 + '|')
            else:
                db.update('user', where="uid='" + self.uid + "'", animelist = animeliststr, \
                isread = ''.join(self.isread), epilook = epilook2)
        except:
            return 'ERROR_SYSTEM'
        else:
            return 0


application = web.application(urls, globals()).wsgifunc()
		
