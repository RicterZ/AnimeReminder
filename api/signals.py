from django.utils import timezone
from models import Track, Subscription
from constants import SUBSCRIPTION_WATCHED, SUBSCRIPTION_WATCHING, SUBSCRIPTION_FORGONE


def update_subscription_signal(sender, **kwargs):
    instance = kwargs['instance']

    if instance.status == SUBSCRIPTION_FORGONE:
        pass
    elif instance.status == SUBSCRIPTION_WATCHED:
        pass
    elif instance.status == SUBSCRIPTION_WATCHING:
        pass
    #Track.objects.create(user=instance.user, subscript=instance, date_watched=timezone.now())
