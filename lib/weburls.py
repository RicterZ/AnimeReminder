from lib.handlers.BaseHandler import WebBaseHandler
from lib.handlers.IndexHandler import *

urls = (
    '/', 'IndexHandler',
    '/login', 'LoginHandler',
    '/reg', 'RegHandler',
    '/my', 'GetUserInfoHandler',
    '/email_reminder_set', 'EmailStatusSetHandler',
    '/get_update_schedule', 'ScheduleGetHandler',
    '/changepw', 'ChangePasswordHandler',
    '/add_anime', 'AddAnimeHandler',
    '/del_anime', 'DelAnimeHandler',
    '/highlight', 'HighLightHandler',
    '/epiedit', 'LookToEpiEditHandler',
    '/exit', 'ExitHandler',
    '/active', 'ActiveHandler',
    '/help', 'HelpHandler',
    '/search', 'SearchHandler',    
    '/(.*)', 'ErrorHandler'
)