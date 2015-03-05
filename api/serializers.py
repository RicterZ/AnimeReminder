from rest_framework import serializers
from models import Anime, Subscription, UserExtension


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ('id', 'aid', 'name', 'intro', 'is_end', 'episode', 'poster_link', 'updated_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'anime', 'is_read', 'currently_read', 'status', 'user')


class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'anime', 'is_read', 'currently_read', 'status')
        read_only_fields = ('user', 'anime')


class UserExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtension
        fields = ('id', 'date_joined', 'is_staff', 'last_login', 'email', 'username', 'password')
        read_only_fields = ('date_joined', 'is_staff', 'last_login', 'username')


class UserExtensionCreateSerializer(UserExtensionSerializer):
    class Meta:
        model = UserExtension
        fields = ('date_joined', 'is_staff', 'last_login', 'email', 'username', 'password')
        read_only_fields = ('date_joined', 'is_staff', 'last_login')

