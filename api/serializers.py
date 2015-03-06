from rest_framework import serializers
from models import Anime, Subscription, User


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ('id', 'aid', 'name', 'description', 'is_end', 'episode', 'poster_link', 'updated_time')


class SearchSerializer(serializers.Serializer):
    aid = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    episode = serializers.IntegerField()
    poster_link = serializers.URLField()
    updated_time = serializers.DateTimeField()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'anime', 'is_read', 'currently_read', 'status', 'user')


class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'anime', 'is_read', 'currently_read', 'status')
        read_only_fields = ('user', 'anime')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'date_joined', 'is_staff', 'last_login', 'email', 'username')
        read_only_fields = ('id', 'date_joined', 'is_staff', 'last_login', 'username')


