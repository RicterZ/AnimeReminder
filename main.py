# -*- coding:utf-8 -*-
from lib.settings import *
from lib.weburls import *

application = web.application(urls, globals()).wsgifunc()

app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()