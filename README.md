AnimeReminder
=============

##新番提醒网站源码   
版本：3.0   
后端基于: uwsgi + web.py
前端基于: jQuery

##新番提醒是免费提供新番提醒服务的平台

##ToDo

RSS for each user.   

###weburls.py

    urls = (
        '/user/[\d]+.xml', 'RSSHandler'
    )
    
###Handlers/RSSHandler.py

    class RSSHandler:
        #do something
        
欢迎贡献代码
