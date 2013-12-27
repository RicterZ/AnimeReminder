from lib.handlers.BaseHandler import *
from lib.handlers.UserHandler import *
from lib.handlers.DataHandler import *
from lib.handlers.ScheduleHandler import *
from lib.handlers.SubScriptionHandler import *
from lib.handlers.HighlightHandler import *

urls = (
    '/login', 'APILoginHandler',
    '/reg', 'APIRegHandler',
    '/get_user_info', 'GetUserInfoHandler',
    '/email_reminder_set', 'EmailStatusSetHandler',
    '/get_update_schedule', 'ScheduleGetHandler',
    '/changepw', 'ChangePasswordHandler',
    '/add_anime', 'AddAnimeHandler',
    '/del_anime', 'DelAnimeHandler',
    '/highlight', 'HighLightHandler',
    '/epiedit', 'LookToEpiEditHandler',
)