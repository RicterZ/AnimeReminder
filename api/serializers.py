from django.db.models import Q
from rest_framework import serializers
from models import Anime, Subscription, User, UserExtension


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        read_only_fields = ('updated_time',)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        read_only_fields = ('user',)


class UserExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtension
        fields = ('date_joined', 'is_staff', 'last_login', 'email', 'username', 'password')
        read_only_fields = ('date_joined', 'is_staff', 'last_login')

