from lib.handlers.common.BaseHandler import APIBaseHandler
from lib.settings import *

class RegHandler(APIBaseHandler):
    def GET(self):
        return returnData(MethodErrorMessage)

    def POST(self):
        webinput = web.input(u='',p='')
        email, password = self.inputClean(webinput.u), webinput.p
        if not (email or password): return returnData(UnknowErrorMessage)
        if len(webinput.p) < 6 or len(webinput.p) > 16:
            return returnData(PasswordFormatMessage)
        password = self.pwToMD5(web.input().p)
        if not self.checkEmail(email): return returnData(EmailErrorMessage)
        data = db.select('user', where="email='%s'"%email)
        if not len(data) == 0: return returnData(EmailExistMessage)

        key = self.makeKey()
        data = db.insert('user',email=email,password=password,emailid='0',keyid=key)
        return returnData(data={"key": key})


class LoginHandler(APIBaseHandler):
    def GET(self):
        return returnData(MethodErrorMessage)

    def POST(self):
        webinput = web.input(u='',p='')
        email, password = self.inputClean(webinput.u), self.pwToMD5(webinput.p)
        if not email or not password: return returnData(UnknowErrorMessage)
        userData = db.select('user', where="email='%s'"%email, what="password,id")
        if userData:
            userData = userData[0] 
        else:
            return returnData(LoginErrorMessage)
        if not password == userData.password: return returnData(LoginErrorMessage)
        key = self.makeKey()
        db.update('user', where="id=%d"%userData.id, keyid=key)
        return returnData(data={"key": key})


class ChangePasswordHandler(APIBaseHandler):
    def GET(self):
        return returnData(MethodErrorMessage)

    def POST(self):
        if not self.isKey: return returnData(KeyErrorMessage)
        webinput = web.input(oldpw='',newpw='')
        oldpw = self.pwToMD5(webinput.oldpw)
        if len(webinput.newpw) < 6 or len(webinput.newpw) > 16:
            return returnData(PasswordFormatMessage)
        newpw = self.pwToMD5(webinput.newpw)
        if not oldpw == self.password: return returnData(LoginErrorMessage)
        db.update('user', where="id=%d"%self.id,password=newpw,keyid='')
        return returnData()