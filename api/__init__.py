from django.db.models.signals import post_save
from models import Subscription
from signals import update_subscription_signal


post_save.connect(update_subscription_signal, sender=Subscription)
