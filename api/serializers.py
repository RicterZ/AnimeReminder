from rest_framework import serializers
from models import Anime, Subscription, User, Season


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ('id', 'name', 'cover', 'default', 'season_id', 'anime', 'count')


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ('id', 'aid', 'name', 'description', 'is_end', 'episode', 'poster_link', 'updated_time')


class AnimeOfSubscriptionSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(many=True)
    class Meta:
        model = Anime
        fields = ('id', 'aid', 'name', 'description', 'is_end', 'episode', 'poster_link', 'updated_time', 'seasons')


class SearchSerializer(serializers.Serializer):
    aid = serializers.IntegerField()
    season_id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    episode = serializers.IntegerField()
    poster_link = serializers.URLField()
    updated_time = serializers.DateTimeField()


class SubscriptionSerializer(serializers.ModelSerializer):
    anime = AnimeOfSubscriptionSerializer()
    class Meta:
        model = Subscription
        fields = ('id', 'anime', 'is_read', 'currently_read', 'status')


class SubscriptionCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()


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

