# -*- coding:utf-8 -*-
#-----------------------------------------------
#新番提醒器Python后端实现部分 by Ricter
#E-mail:canyuexiaolang@gmail.com
#Website:http://www.ricter.info
#-----------------------------------------------

from lib.anime import new_anime
import urllib ,urllib2
import re, os, datetime
import zipfile, random, hashlib
import web
import jinja2 as jj

########################设置#########################
dbhost  = '127.0.0.1'             ##数据库地址     ##
dbtype  = 'mysql'                 ##数据库类型     ##
dbname  = '                       ##数据库名       ##
dbun    = ''                      ##数据库用户名   ##
dbpw    = ''                      ##数据库密码     ##
luadir = 'animelua'               ##Lua下载目录设置##
tempdir = '../templates'          ##模板目录设置   ##
########################设置#########################

global db
db = web.database(host=dbhost, dbn=dbtype, db=dbname, user=dbun, pw=dbpw)        #连接数据库
os.chdir(luadir)                                                                 #cd到下载lua文件的目录
env = jj.Environment(loader = jj.FileSystemLoader(tempdir))                      #模板渲染
web.config.debug = False                                                        #关闭调试模式

urls=(
    '/', 'IndexHandler',
    '/my', 'UserHandler',
    '/search', 'SearchHandler',
    '/get_schedule', 'AjaxScheduleHandler',
    '/delhighlight', 'DelHighlightHandler',
    '/addhighlight', 'AddHighlightHandler',
    '/ajaxsearch', 'AjaxSearchHandler',
    '/delanime', 'AjaxDelAnimeHandler',
    '/addanime', 'AjaxAddAnimeHandler',
    '/login', 'LoginHandler',
    '/reg', 'RegHandler',
    '/help', 'HelpHandler',
    '/changeremind', 'ReminderStatChangeHandler',
    '/epiedit', 'EpiEditHandler',
    '/exit', 'ExitHandler',
    '/active', 'ActiveHandler',
    '/(.*)', 'ErrorHnadler'
)

class BaseHandler:
    """基础类，实现共同功能减少代码量"""

    isLogin = False
    uid = ''
    session = ''
    updateNum = '0'

    def __init__(self):
        """
        子类继承时预处理，完成包括实现判断是否登陆以及定义各种用户数据的功能
        """
        web.header('Content-type', "text/html; charset=utf-8")                       #设置HTTP头，防止返回乱码或者纯HTML代码
        try:                                                                         #检测是否登录，返回bool值
            c_uid, c_session = web.cookies().uid, web.cookies().session              #在cookie内获取uid，session
            user_data = db.query('select * from user where uid="' + c_uid + '"')[0]  #连接服务器获取用户session
            session, updateNum = user_data.session, str(list(user_data.isread).count('1') + list(user_data.isread).count('2'))
            animeList, readList = user_data.animelist, list(user_data.isread)
            isRemind = user_data.isremind
            epilook, isRead = user_data.epilook, user_data.isread                    #各种从数据库读数据
            if not str(session) == str(c_session):self.isLogin = False               #对比session，防止注入登录
        except:
            self.isLogin = False                                                     #用户未登陆
        else:
            self.isLogin = True                                                      #用户已登陆
            self.uid = c_uid
            self.session = c_session
            self.updateNum = updateNum
            self.readList = readList
            self.animeList = animeList
            self.isRead = isRead
            self.isRemind = isRemind
            self.epilook = epilook                                                   #基础类各种用户数据

    def render(self, templatefile, title='动漫更新表'.decode('utf8'), **kwargs):
        """
        连接模板方法，供子类调用
        """
        return env.get_template(templatefile).render(title=title, **kwargs)          #返回值到模板，其中返回字典可直接在模板中{{% name %}}调用

    def HightlightSetting(self, stat):
        """
        高亮设置方法，传入'0'(不高亮)或者'1'(高亮)。
        """
        try:
            animeid = str(int(web.input().aid))
            self.readList[self.animeList.split('|')[:-1].index(animeid)] = stat         #设置高亮与否
            db.update('user', where="uid=" + self.uid, isRead = ''.join(self.readList)) #连接数据库，更新内容
        except:
            return 'ERROR'                                                              #若出错返回错误
        else:
            return '0'                                                                  #成功即返回0，供ajax调用

class IndexHandler(BaseHandler): 
    """
    IndexHandler类是处理主页请求类，继承于BaseHandler类
    """
    def GET(self):
        data, animeList = db.query('select * from anmielist where 1 order by id desc limit 0,9'), []  #连接数据库，取前8个动漫数据用来在首页显示
        for i in data:                                             #生成动漫数据列表，格式为[[动漫名, 动漫id, 动漫集数, 是否为更新动漫, 是否完结]]
            animeList.append([i.animename, i.animeid, i.episode, i.isnew, i.isover])                   #二维表格以便于处理

        return self.render('animeList.html', '动漫更新表'.decode('utf8'), animeList = animeList, \
        isLogin = self.isLogin, uid = self.uid, newnum = self.updateNum)                               #返回值，部署到模板以显示

class LoginHandler(BaseHandler):
    def GET(self):
        try:
            aid = str(int(web.input().aid))
        except:
            aid = '0'
            goto = False
        else:
            goto = True

        if self.isLogin:
            return self.render('error.html', '错误'.decode('utf8'), errinfo = 'You had logined.', \
            isLogin = self.isLogin, newnum = self.updateNum)

        if goto:
            return self.render('login.html', '登录'.decode('utf8'), isLogin = self.isLogin, aid = aid)
        else:
            return self.render('login.html', '登录'.decode('utf8'), isLogin = self.isLogin)

    def POST(self):
        try:
            email = web.input().username.replace('"', '').replace("'", '')
            password = web.input().password
            if len(password) < 6 and len(password) > 16:
                return self.render('error.html', "Error", errinfo='邮箱或密码错误'.decode('utf8'), \
                isLogin = self.isLogin, newnum = self.updateNum)
            if len(email) > 50:
                return self.render('error.html', "Error", errinfo='邮箱或密码错误'.decode('utf8'), \
                isLogin = self.isLogin, newnum = self.updateNum)
            passwordhash = hashlib.md5()
            passwordhash.update(password)
            password = passwordhash.hexdigest()
        except Exception, e:
            return self.render('error.html', "错误".decode('utf8'), errinfo= e, \
            isLogin = self.isLogin, newnum = self.updateNum)

        try:
            aid = str(int(web.input().aid))
        except:
            isadd = False
        else:
            isadd = True

        #检查是否存在用户
        data = db.query('select * from user where email="' + email + '"')
        if len(data) == 0:
            return self.render('error.html', "错误".decode('utf8'), errinfo=\
            '用户不存在&nbsp;<a href="/reg">注册>></a>'.decode('utf8'), 
            isLogin = self.isLogin, newnum = self.updateNum)

        #检查是否激活
        if not int(data[0].emailid) == 0:
            return self.render('error.html', "错误".decode('utf8'), errinfo='用户未激活'.decode('utf8'), \
            isLogin = self.isLogin, newnum = self.updateNum)

        data = db.query('select * from user where email="' + email + '"')
        t = data[0]
        psw =  t.password
        if not psw == password:
            return self.render('error.html', "错误".decode('utf8'), errinfo='邮箱或密码错误'.decode('utf8'), \
            isLogin = self.isLogin, newnum = self.updateNum)

        uid = t.uid
        session = 'R_' + str(random.randrange(1000000,9999999))

        try:
            db.update('user', where="uid=" + uid, session = session)
            web.setcookie('uid', uid, 10000000)
            web.setcookie('email', email, 10000000)
            web.setcookie('session', session, 10000000)
        except:
            return self.render('error.html', "错误".decode('utf8'), errinfo=\
            '系统错误，有可能您已禁止Cookies，或联系系统管理员'.decode('utf8'),
            isLogin = self.isLogin, newnum = self.updateNum)

        if not isadd:
            return web.seeother('/my')
        else:
            return web.seeother('/addanime?isgoto=0&aid=' + aid)

class RegHandler(BaseHandler):
    def GET(self):
        if self.isLogin:
            return self.render('error.html', '错误'.decode('utf8'), errinfo = 'You had logined.', \
            isLogin = self.isLogin, newnum = self.updateNum)

        return self.render('reg.html', '注册'.decode('utf8'), isLogin = self.isLogin)

    def POST(self):
        if self.isLogin:
            return self.render('error.html', '错误'.decode('utf8'), errinfo = 'You had logined.', \
            isLogin = self.isLogin, newnum = self.updateNum)

        try:
            email = web.input().email.replace('"', '').replace("'", '').replace('>', '').replace('<', '')
            password = web.input().password
            password2 = web.input().password2
            if not '@' in email or not '.' in email:
                return self.render('error.html', '错误'.decode('utf8'), errinfo = '注册时输错：电子邮箱非法'.decode('utf8'), \
                isLogin = self.isLogin)
            if email.find('@') == -1:
                return self.render('error.html', '错误'.decode('utf8'), errinfo = '注册时输错：电子邮箱非法'.decode('utf8'), \
                isLogin = self.isLogin)
            if len(email) > 50:
                return self.render('error.html', '错误'.decode('utf8'), errinfo = '注册时输错：电子邮箱过长'.decode('utf8'), \
                isLogin = self.isLogin)
            if len(password) < 6:
                return self.render('error.html', '错误'.decode('utf8'), errinfo = '注册时输错：密码过短'.decode('utf8'), \
                isLogin = self.isLogin)
            if len(password) > 16:
                return self.render('error.html', '错误'.decode('utf8'), errinfo = '注册时输错：密码过长'.decode('utf8'), \
                isLogin = self.isLogin)
            if not password == password2:
                return self.render('error.html', '错误'.decode('utf8'), errinfo = '注册时输错：两次输入的密码不同'.decode('utf8'), \
                isLogin = self.isLogin)
        except AttributeError:
            return self.render('error.html', '错误'.decode('utf8'), errinfo = 'DATA ERROR', \
            isLogin = self.isLogin)

        uid = str(random.randrange(1000000,9999999)) + str(random.randrange(1000000,9999999))

        #检查UID是否重复
        data = db.query('select uid from user where uid="' + uid + '"')
        while not len(data) == 0:
            uid = str(random.randrange(1000000,9999999)) + str(random.randrange(1000000,9999999))
            data = db.query('select uid from user where uid="' + uid + '"')

        #检查邮箱是否重复
        data = db.query('select uid from user where email="' + email + '"')
        if not len(data) == 0:
            return self.render('error.html', '错误'.decode('utf8'), errinfo = '注册时输错：邮箱已被注册'.decode('utf8'), \
            isLogin = self.isLogin)

        #密码md5散列处理
        h = hashlib.md5()
        h.update(password)
        password = h.hexdigest()

        #邮箱激活认证ID
        emailid = str(random.randrange(1000000,9999999)) + str(random.randrange(1000000,9999999))

        #连接数据库
        data = db.insert('user', email = email, password = password, emailid = emailid, uid = uid)

        #发送邮件
        web.sendmail(
            'AnimeReminderActive', 
            email, 
            'Anime Reminder 新番提醒器激活通知', 
            '请点击下面的链接激活：http://anime.ricter.info/active?uid=' + uid + '&emailid=' + emailid, 
            headers={'Content-Type':'text/html;charset=utf-8','User-Agent': 'webpy.sendmail', 'X-Mailer': 'webpy.sendmail'}
        )

        return self.render('error.html', '信息', errinfo = '请进入邮箱打开链接进行激活，如未收到邮件，请联系canyuexiaolang@gmail.com'\
            .decode('utf8'), isLogin = self.isLogin)

class UserHandler(BaseHandler):
    """
    处理用户界面请求
    """
    def GET(self):
        if not self.isLogin:
            return web.seeother('/')                                                                          #判断是否登录
        useranimeList, lookList, lookRecode = self.animeList, list(self.isRead), self.epilook[:-1].split('|') #从类定义（我怎么感觉多此一举了）
        highlightList, normalList = [], []
        if len(useranimeList) > 0:                                                                            #判断是否有订阅列表
            useranimeList = useranimeList.split('|')[:-1]                                                     #若有删除最后的“|”，拆分字符串为列表
            for id in useranimeList:                                                                          #循环id值
                t = db.query('select * from anmielist where animeid="' + id + '"')[0]                         #以id值查询数据库
                if str(lookList[useranimeList.index(id)]) == '0':                                             #判断是否为高亮
                    normalList.append([t.animename, t.animeid, t.episode, t.isover, \
                    lookRecode[useranimeList.index(t.animeid)]])                                              #normalList
                else:
                    highlightList.append([t.animename, t.animeid, t.episode, \
                    t.isover, lookRecode[useranimeList.index(t.animeid)]])                                    #若为高亮动漫加入highlightList

        return self.render('userlist.html', "我的订阅".decode('utf8'), highlightList = highlightList, \
        normalList = normalList, isLogin = self.isLogin, newnum = self.updateNum, isRemind = self.isRemind)   #部署到模板

class SearchHandler(BaseHandler):
    """
    处理动漫查找页面的请求
    """
    def GET(self):
        xunlei = new_anime()
        try:
            animename = None                                                           #定义animename为None，防止无参数提交
            animename = web.input().n                                                  #获取用户输入
        except:
            web.seeother('/')

        if animename:
            return self.render('search.html', "搜索结果".decode('utf8'), searchResultList = \
            xunlei.animeSearch(animename.encode('gbk')), \
            isLogin = self.isLogin, newnum = self.updateNum)                           #xunlei.animeSearch(animename.encode('gbk'))即是结果

class AjaxSearchHandler(BaseHandler):
    def GET(self):
        try:
            animename = web.input().n
        except:
            animename = ''
        xunlei = new_anime()
        return self.render('ajaxsearch.html', searchlist = xunlei.animeSearch(animename.encode('utf8')))

class AjaxScheduleHandler(BaseHandler):
    """
    新番更新时间表爬虫Beta
    实现方法是爬迅雷看看动漫官网的HTML代码，正则表达式解析获取更新时间表
    """
    def GET(self):
        xunlei = new_anime()                                                                               #调用传说中的AnimeClass了喵哈哈哈哈
        url = 'http://anime.kankan.com/'                                                                   #定义地址
        reqdata = xunlei.getURL(url)                                                                       #访问url，返回html代码

        animeList, todaylist, tomorrowlist = [], [], []
        try:
            updatelist = re.compile(r'<li>\d\d:\d\d.*<a.*')                                                #定义正则，获取更新的列表
            updatetime = re.compile(r'<ul id="sche_show_\d">')                                             #定义正则，获取更新的日期（0-6表示周日-周六）
            time = re.compile(r'\d\d:\d\d')                                                                #定义正则，获取更新的时间
            href = re.compile(r'http://.*\d\d\d\d\d')                                                      #定义正则，获取动漫的链接
            name = re.compile(r'">.*</a>')                                                                 #定义正则，获取动漫的名称
            for i in reqdata.split('\n'):                                                                  #以换行符拆分HTML代码
                if updatetime.findall(i): weakday = updatetime.findall(i)[0].split('"')[1].split('_')[2]   #正则获取更新的日期
                if updatelist.findall(i):
                    data = updatelist.findall(i)[0].decode('utf8')                                         #正则获取更新的内容
                    anime = weakday + '|' + time.findall(data)[0] + '|' + href.findall(data)[0] \
                    + '|' + name.findall(data)[0].strip('">').split('<')[0]  #生成字符串，格式为：更新日期|更新时间|动漫Url|动漫名称
                    animeList.append(anime)                                  #加入列表中
            d = datetime.datetime.now()                                      #获取今日日期
            today = d.weekday() + 1                                          #今日日期数+1，代表今天（对，你没看错，datetime获取的日期和迅雷上的正好相差1）
            torro = d.weekday() + 2                                          #今日日期数+2，代表明天
            if today == 7: today = 0                                         #如果今天是周日，今天为0（正好是迅雷看看上0代表周日）
            if torro >= 7: torro = torro - 7                                 #如果今天是周日，明天就是今天-7，这个算法想想就出来了
            for i in animeList:                                              #在这里加入列表
                if i.split('|')[0] == str(today):
                    todaylist.append(i)
                if i.split('|')[0] == str(torro):
                    tomorrowlist.append(i)
        except:
            return 'ERROR_GET_LIST'                                          #出错返回ERROR
        else:
            return self.render('schedule.html', "Schedule", todaylist = todaylist, tomorrowlist = tomorrowlist)

class AjaxDelAnimeHandler(BaseHandler):
    """
    处理Ajax方式访问删除动漫的请求
    """
    def GET(self):
        if self.isLogin == False:                                              #判断是否登录
            return 'ERROR_NOT_LOGIN'

        try:
            animeid = str(int(web.input().aid))                                #获取动漫ID
        except:
            return 'ERROR_ANIME_ID'

        try:
            epilook2 = ''
            self.epilook = self.epilook.split('|')[:-1]                        #拆分epilook为列表并去除列表最后一项（Null）
            self.readList[self.animeList.split('|')[:-1].index(animeid)] = ''  #readList的所删除动漫处的内容删除
            self.epilook[self.animeList.split('|')[:-1].index(animeid)] = ''   #epilook的所删除动漫处的内容删除
            for i in self.epilook:
                if i and epilook2:epilook2 = epilook2 + '|' + i                #格式处理，由列表变成字符串
                if i and not epilook2:epilook2 = i                             #此处？忘记了
        except Exception, e:
            epilook2 = '|'.join(self.epilook)

        self.animeList = self.animeList.replace(animeid + '|', '')             #此处为订阅动漫的删除
        if epilook2:
            db.update('user', where="uid=" + self.uid, animelist = self.animeList, \
            isread = ''.join(self.readList), epilook = epilook2 + '|')
        else:
            db.update('user', where="uid=" + self.uid, animelist = self.animeList, \
            isread = ''.join(self.readList), epilook = epilook2)               #更新到数据库
        return '0'

class AjaxAddAnimeHandler(BaseHandler):
    def GET(self):
        if self.isLogin == False:                                              #判断是否登录
            return 'ERROR_NOT_LOGIN'

        try:
            animeid = str(int(web.input().aid))                                #获取动漫id
        except:
            return 'ERROR_ANIME_ID'

        try:                                                                   #未登录时添加需要跳转到我的订阅
            isgoto = web.input().isgoto
        except:
            isgoto = False
        else:
            isgoto = True

        addData = False                                                        #这三行实现的功能是判断动漫是否在数据库内，若没有就添加
        data = db.query('select * from anmielist where animeid="' + animeid + '"')
        if len(data) == 0:addData = True

        if addData:                                                            #动漫添加实现部分
            xunlei = new_anime()
            epinum = xunlei.getNewEpisode(animeid)                             #epinum为返回值，若为int则证明不是动漫或者动漫不存在，若为list则获取成功
            #print epinum                                                      #调试时使用，这里注释掉
            if isinstance(epinum, int):                                        #isinstance判断是否为int
                return 'ERROR_INVALID_ANIME'
            else:
                #1 is over ; 0 is not over
                epi, isoverbool = epinum[0], epinum[1]                         #epinum返回值为[动漫集数, 是否完结]
                #print animeid, epi, isoverbool                                调试时使用，这里注释掉
                if int(epi) > 0:                                               #大于1即是判断是否为电影（1）
                    data = db.insert('anmielist', animename=(xunlei.\
                    getNameByID(animeid).strip('"')),animeid=animeid,episode=epi, isover=isoverbool) #加入数据库
                else:
                    return 'ERROR_INVALID_ANIME'

        try:
            if not animeid in self.animeList:
                db.update('user', where="uid=" + self.uid, animelist = animeid + '|' \
                + self.animeList, isread = '0' + self.isRead, epilook = '0|' + self.epilook) #加入用户数据
        except Exception, e:
            return 'ERROR_SYSTEM:' + str(e)

        if isgoto:
            return web.seeother('/my')
        else:
            return '0'

class ReminderStatChangeHandler(BaseHandler):
    def GET(self):
        if not self.isLogin:
            return web.seeother('/')

        try:
            i = '0'
            i = str(int(web.input().i))
        except:
            return web.seeother('/')

        if int(i) == 0:
            db.update('user', where="uid=" + self.uid, isremind = 0)
        else:
            db.update('user', where="uid=" + self.uid, isremind = 1)
			
        return web.seeother('/my')

class EpiEditHandler(BaseHandler):
    def GET(self):
        if not self.isLogin:
            return 'ERROR_NOT_LOGIN'

        try:
            animeid = str(int(web.input().aid))
            epinum = str(int(web.input().epi))
            data = db.query('select * from anmielist where animeid="' + animeid + '"')
            episode = data[0].episode
        except:
            return 'ERROR_ANIME'

        animeList = self.animeList[:-1].split('|')
        if not animeid in animeList:return 'ERROR_ANIME'
        if int(episode) < int(epinum) or int(epinum) < 0:return 'ERROR_EPI'
        try:
            epilook = self.epilook.split('|')[:-1]
            epilook[animeList.index(animeid)] = epinum
            epistr = '|'.join(epilook) + '|'
            print epilook, epistr
            db.update('user', where="uid=" + self.uid, epilook = epistr)
            return '0'
        except:
            return 'ERROR_SYSTEM'

class AddHighlightHandler(BaseHandler):
    """
    设置动漫高亮
    外部访问需传入动漫id
    """
    def GET(self):
        if not self.isLogin:
            return 'ERROR_NOT_LOGIN'                                           #判断是否登陆
        return self.HightlightSetting('1')                                     #调用方法

class DelHighlightHandler(BaseHandler):
    """
    取消动漫高亮
    外部访问需传入动漫id
    """
    def GET(self):
        if not self.isLogin:
            return 'ERROR_NOT_LOGIN'                                           #判断是否登陆
        return self.HightlightSetting('0')                                     #调用方法

class ActiveHandler(BaseHandler):
    def GET(self):
        if self.isLogin:
            return self.render('error.html', 'Error', errinfo = 'You had logined.', \
            isLogin = self.isLogin, newnum = self.updateNum)

        try:
            #接收参数，其实这里起到防注入功能了
            uid = str(int(web.input().uid))
            eid = str(int(web.input().emailid))
        except:
            return self.render('error.html', 'Error', errinfo = 'DATA ERROR', \
            isLogin = self.isLogin)

        #检查UID是否存在
        data = db.query('select * from user where uid="' + uid + '"')
        if len(data) == 0:
            return self.render('error.html', 'Error', errinfo = '激活时输错：UID不存在'.decode('utf8'), \
            isLogin = self.isLogin)

        #检查EID是否正确
        if not int(eid) == int(data[0].emailid):
            return self.render('error.html', 'Error', errinfo = '激活时输错：EID不符合，请到邮箱重新打开链接'\
            .decode('utf8'), isLogin = self.isLogin)

        db.update('user', where="uid=" + uid, emailid = '0')
        return self.render('error.html', 'Infomation', errinfo = '激活成功，请<a href="/login">登录</a>>>'\
            .decode('utf8'), isLogin = self.isLogin)

class HelpHandler(BaseHandler):
    """
    处理用户帮助页请求类
    """
    def GET(self, *argv):
        return self.render('help.html', "帮助与支持".decode('utf8'), isLogin = self.isLogin, \
        newnum = self.updateNum)

class ErrorHnadler(BaseHandler):
    """
    处理错误请求
    """
    def GET(self, *argv):
        return self.render('error.html', '错误'.decode('utf8'), errinfo = '404 Error', \
        isLogin = self.isLogin, newnum = self.updateNum)

class ExitHandler:
    """
    处理退出请求
    """
    def GET(self):
        web.setcookie('uid', 0, -1)
        web.setcookie('email', 0, -1)
        web.setcookie('session', 0, -1)
        return web.seeother('/')

#app = web.application(urls, globals())
#if __name__ == "__main__":app.run()

application = web.application(urls, globals()).wsgifunc()
