# -*- coding:utf-8 -*-
from lib.apiurls import *

application = web.application(urls, globals()).wsgifunc()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

