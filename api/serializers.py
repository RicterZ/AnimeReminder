from rest_framework import serializers
from rest_framework import validators
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
        fields = ('id', 'anime', 'currently_read', 'status', 'season')


class SubscriptionCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    def get_fields(self):
        fields = super(SubscriptionUpdateSerializer, self).get_fields()
        # filter seasons of the anime
        fields['season'].queryset = Season.objects.filter(anime=self.instance.anime)
        return fields

    class Meta:
        model = Subscription
        fields = ('id', 'anime', 'currently_read', 'status', 'season')
        read_only_fields = ('user', 'anime')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'date_joined', 'is_staff', 'last_login', 'email', 'username')
        read_only_fields = ('id', 'date_joined', 'is_staff', 'last_login', 'username')
