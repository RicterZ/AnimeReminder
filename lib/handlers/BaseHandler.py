# -*- coding:utf-8 -*-
from lib.settings import *

class BaseHandler:
    def inputClean(self, inputData):
        return inputData.replace("'", '').replace('"', '').replace('\\', '')\
                        .replace('/', '').replace('?', '').replace(' ', '')

    def pwToMD5(self, pwstr):
        h = hashlib.md5()
        h.update(pwstr)
        return h.hexdigest()

    def checkEmail(self, emailStr):
        return '@' in emailStr and '.' in emailStr and \
                not emailStr.find('@') == -1

    def makeKey(self):
        while True:
            key = ''.join(random.sample(string.letters+string.digits, 20))
            if len(db.select('user', where="keyid='%s'"%key))==0: return key


class APIBaseHandler(BaseHandler):

    def __init__(self):
        try:
            key            = self.inputClean(web.input().key)
            if not key: raise Exception("KeyError")
            userData       = db.select('user', where="keyid='%s'"%key)[0]
            self.id        = userData.id
            self.password  = userData.password
            self.animestr  = userData.animelist
            self.animelist = userData.animelist.split('|')[:-1]
            self.epistr    = userData.epilook
            self.epilook   = userData.epilook.split('|')[:-1]
            self.isread    = list(userData.isread)
            self.isreadstr = userData.isread
            self.isremind  = userData.isremind
            self.isKey     = True
        except:
            self.isKey = False
        web.header('Content-type', "application/json; charset=utf-8")





class WebBaseHandler(BaseHandler):

    def __init__(self):
        try:  
            c_id, key = web.cookies().id, self.inputClean(web.cookies().session)
            userData       = db.select('user', where="session='%s'"%key)[0]
            self.uid       = userData.id
            self.email     = userData.email
            self.password  = userData.password
            self.animestr  = userData.animelist
            self.animelist = userData.animelist.split('|')[:-1]
            self.epistr    = userData.epilook
            self.epilook   = userData.epilook.split('|')[:-1]
            self.isread    = list(userData.isread)
            self.isreadstr = userData.isread
            self.isremind  = userData.isremind
            self.isLogin   = True
            self.updateNum = list(userData.isread).count('1')
        except Exception, e:
            self.isLogin   = False
            self.updateNum = 0
            self.uid       = 0
        web.header('Content-type', "application/json; charset=utf-8")
