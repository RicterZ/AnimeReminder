from lib.handlers.BaseHandler import *
from lib.handlers.IndexHandler import *
from lib.handlers.UserHandler import *
from lib.handlers.SubScriptionHandler import *
from lib.handlers.DataHandler import *
from lib.handlers.HighlightHandler import *
from lib.handlers.ScheduleHandler import *

urls = (
    '/', 'gotoIndex',
    '/index', 'IndexHandler',
    '/check', 'CheckHandler',
    '/login', 'LoginHandler',
    '/reg', 'RegHandler',
    '/my', 'WebGetUserInfoHandler',
    '/email_reminder_set', 'WebEmailStatusSetHandler',
    '/get_update_schedule', 'ScheduleGetHandler',
    '/changepw', 'ChangePasswordHandler',
    '/add_anime', 'AddAnimeHandler',
    '/del_anime', 'DelAnimeHandler',
    '/highlight', 'HighLightHandler',
    '/epiedit', 'LookToEpiEditHandler',
    '/exit', 'ExitHandler',
    '/search', 'SearchHandler', 
)