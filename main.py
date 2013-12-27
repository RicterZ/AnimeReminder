# -*- coding:utf-8 -*-
#-----------------------------------------------
#新番提醒器Python后端实现部分 by Ricter
#E-mail:canyuexiaolang@gmail.com
#Website:http://www.ricter.info
#-----------------------------------------------
from lib.handlers.BaseHandler import WebBaseHandler
from lib.settings import *
from lib.weburls import *

class LoginHandler(WebBaseHandler):
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

class RegHandler(WebBaseHandler):
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

class UserHandler(WebBaseHandler):
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



class ActiveHandler(WebBaseHandler):
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

class HelpHandler(WebBaseHandler):
    """
    处理用户帮助页请求类
    """
    def GET(self, *argv):
        return self.render('help.html', "帮助与支持".decode('utf8'), isLogin = self.isLogin, \
        newnum = self.updateNum)

class ErrorHandler(WebBaseHandler):
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

app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()

#application = web.application(urls, globals()).wsgifunc()
