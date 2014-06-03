from django.db.models import Q
from rest_framework import serializers
from models import Anime, Subscription, User


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        read_only_fields = ('updated_time',)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        read_only_fields = ('user',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def validate(self, attrs):
        return attrs