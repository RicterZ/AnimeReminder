from lib.handlers.common import *
from lib.handlers.web import *

urls = (
    '/', 'IndexPage',
    '/user', 'UserPage',
    '/index', 'IndexDataHandler',
    '/check', 'CheckHandler',
    '/login', 'LoginHandler',
    '/reg', 'RegHandler',
    '/my', 'GetUserInfoHandler',
    '/email_reminder_set', 'EmailStatusSetHandler',
    '/get_update_schedule', 'ScheduleGetHandler',
    '/changepw', 'ChangePasswordHandler',
    '/add_anime', 'AddAnimeHandler',
    '/del_anime', 'DelAnimeHandler',
    '/highlight', 'WebHighLightHandler',
    '/epiedit', 'EpiEditHandler',
    '/exit', 'ExitHandler',
    '/search', 'SearchHandler', 
)