from lib.handlers.common import *
from lib.handlers.api import *

urls = (
    '/login', 'LoginHandler',
    '/reg', 'RegHandler',
    '/get_user_info', 'GetUserInfoHandler',
    '/email_reminder_set', 'EmailStatusSetHandler',
    '/get_update_schedule', 'ScheduleGetHandlerV2',
    '/changepw', 'ChangePasswordHandler',
    '/add_anime', 'AddAnimeHandler',
    '/del_anime', 'DelAnimeHandler',
    '/highlight', 'HighLightHandler',
    '/epiedit', 'EpiEditHandler',
)