#coding: utf-8
#暂时决定用不到的东西
from lib.handlers.BaseHandler import WebBaseHandler

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