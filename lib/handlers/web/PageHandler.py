# -*- coding:utf-8 -*-
from lib.handlers.common.BaseHandler import WebBaseHandler
from lib.settings import *

class IndexPage(WebBaseHandler):
    def GET(self):
        web.header('Content-type', "text/html; charset=utf-8")
        return self.render('index.html', title = '主页'.decode('utf-8'))


class UserPage(WebBaseHandler):
    def GET(self):
        web.header('Content-type', "text/html; charset=utf-8")
        return self.render('my.html', title = '我'.decode('utf-8'))