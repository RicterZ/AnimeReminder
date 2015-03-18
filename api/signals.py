from django.utils import timezone
from models import Track, Subscription
from constants import SUBSCRIPTION_WATCHED, SUBSCRIPTION_WATCHING, SUBSCRIPTION_FORGONE, \
    TRACK_ADD, TRACK_FORGONE, TRACK_WATCHED, SUBSCRIPTION_UNWATCHED


def update_subscription_signal(sender, **kwargs):
    instance = kwargs['instance']
    if instance.status == SUBSCRIPTION_FORGONE:
        message = TRACK_FORGONE
    elif instance.status == SUBSCRIPTION_WATCHING:
        if instance.currently_watched == instance.currently_watched:
            return
        message = instance.currently_watched
    elif instance.status == SUBSCRIPTION_WATCHED:
        message = TRACK_WATCHED
    else:
        # fallback
        instance.status = SUBSCRIPTION_WATCHING
        message = instance.currently_watched

    if not Track.objects.filter(subscription=instance):
        instance.status = SUBSCRIPTION_UNWATCHED
        message = TRACK_ADD

    Track.objects.create(user=instance.user, subscription=instance,
                         season=instance.season, date_watched=timezone.now(),
                         status=instance.status, message=message)
