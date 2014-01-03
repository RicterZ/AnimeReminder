from lib.handlers.BaseHandler import *
from lib.handlers.IndexHandler import *
from lib.handlers.UserHandler import *
from lib.handlers.SubScriptionHandler import *
from lib.handlers.DataHandler import *
from lib.handlers.HighlightHandler import *
from lib.handlers.ScheduleHandler import *
from lib.handlers.PageHandler import *
from lib.handlers.SearchHandler import *

urls = (
    '/', 'IndexPage',
    '/user', 'UserPage',
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
    '/highlight', 'WebHighLightHandler',
    '/epiedit', 'EpiEditHandler',
    '/exit', 'ExitHandler',
    '/search', 'SearchHandler', 
)