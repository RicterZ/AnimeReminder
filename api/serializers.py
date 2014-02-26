from rest_framework.serializers import ModelSerializer
from models import Anime, Subscription, User


class AnimeSerializer(ModelSerializer):
    class Meta:
        model = Anime
        read_only_fields = ('updated_time',)


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        read_only_fields = ('user',)

    def validate(self, attrs):
        return attrs


class UserSerializer(ModelSerializer):
    class Meta:
        model = User