from lib.handlers.common.BaseHandler import WebBaseHandler
from lib.settings import *

class LoginHandler(WebBaseHandler):
    def POST(self):
        webinput = web.input(u='',p='')
        email, password = self.inputClean(webinput.u), self.pwToMD5(webinput.p)
        if not email or not password: return returnData(500, UnknowErrorMessage)
        userData = db.select('user', where="email='%s'"%email, what="password,id")
        if userData:
            userData = userData[0] 
        else:
            return returnData(500, LoginErrorMessage)
        if not password == userData.password: return returnData(500, LoginErrorMessage)
        key = self.makeKey()
        db.update('user', where="id=%d"%userData.id, session=key)
        web.setcookie('id', userData.id, 10000000)
        web.setcookie('email', email, 10000000)
        web.setcookie('session', key, 10000000)
        return returnData()


class RegHandler(WebBaseHandler):
    def POST(self):
        webinput = web.input(u='',p='')
        email, password = self.inputClean(webinput.u), webinput.p
        if not (email or password): return returnData(500, UnknowErrorMessage)
        if len(webinput.p) < 6 or len(webinput.p) > 16:
            return returnData(500, PasswordFormatMessage)
        password = self.pwToMD5(web.input().p)
        if not self.checkEmail(email): return returnData(500, EmailErrorMessage)
        data = db.select('user', where="email='%s'"%email)
        if not len(data) == 0: return returnData(500, EmailExistMessage)

        key = self.makeKey()
        data = db.insert('user',email=email,password=password,emailid='0',session=key)
        userData = db.select('user', where="email='%s'"%email, what="id")[0]
        web.setcookie('id', userData.id, 10000000)
        web.setcookie('email', email, 10000000)
        web.setcookie('session', key, 10000000)
        return returnData()


class CheckHandler(WebBaseHandler):
    def POST(self):
        webinput = web.input(id='',session='')
        uid, session = self.inputClean(webinput.id), self.inputClean(webinput.session)
        if not uid or not session: return returnData(500, UnknowErrorMessage)
        userData = db.select('user', where="id=%s"%uid, what="session")
        if userData:
            userData = userData[0] 
        else:
            return returnData(500, LoginErrorMessage)
        if not session == userData.session: return returnData(500, LoginErrorMessage)
        return returnData()


class ExitHandler:
    def GET(self):
        web.setcookie('uid', '', -1)
        web.setcookie('email', '', -1)
        web.setcookie('session', '', -1)
        return web.seeother('/')