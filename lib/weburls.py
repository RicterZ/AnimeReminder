from lib.handlers.common import *
from lib.handlers.web import *

urls = (
    '/', 'IndexPage',
    '/user', 'UserPage',
    '/index', 'IndexDataHandler',
    '/check', 'CheckHandler',
    '/login', 'LoginHandler',
    '/reg', 'RegHandler',
    '/rss/([\d]+).xml', 'RSSHandler',
    '/my', 'GetUserInfoHandler',
    '/email_reminder_set', 'EmailStatusSetHandler',
    '/get_update_schedule', 'ScheduleGetHandler',
    '/changepw', 'ChangePasswordHandler',
    '/add_anime', 'AddAnimeHandler',
    '/del_anime', 'DelAnimeHandler',
    '/highlight', 'HighLightHandler',
    '/epiedit', 'EpiEditHandler',
    '/exit', 'ExitHandler',
    '/search', 'SearchHandler', 
    '/data/(\d{5})', 'AnimeHandler',
)