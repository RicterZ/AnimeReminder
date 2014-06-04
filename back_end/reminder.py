"""
Update all animation, and send a mail to those who have `email` and the `email` was be verified.
"""
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_anime.settings")

from django.db.models import Q
from api.models import Anime, Subscription, UserExtension
from back_end.parse_kankan import get_anime_detail

updated_anime = []
anime_list = Anime.objects.filter(is_end=False)
for anime in anime_list:
    anime_data = get_anime_detail(anime.aid)
    print '[*] Checking: %s ...' % anime.name
    if int(anime_data['episode']) > anime.episode:
        print '[+] ... The latest episode is %s' % anime_data['episode']
        Anime.objects.filter(aid=anime.aid).update(**anime_data)
        Subscription.objects.filter(anime=anime).update(is_read=False)
        updated_anime.append(anime)


users_list = UserExtension.objects.filter(Q(is_email_verified=True) & Q(is_email_reminder=True))
for user in users_list:
    updated_list = Subscription.objects.extra(where=['anime in %s' % str(map(lambda m: m.aid, anime_list))])
    email_content = map(lambda x: '%s, %s' % (x.name, x.episoid), updated_list).join('\n')
    print email_content
    # send email to user
