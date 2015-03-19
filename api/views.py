import copy
from itertools import groupby
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from back_end.bilibili import get_anime_detail, search

from models import Anime, Subscription, User, Season, Track
from permission import ReadOnly, IsOwner, IsAuthenticated, IsSelf, AllowAny
from serializers import AnimeSerializer, SubscriptionSerializer, UserSerializer, \
    UserCreateSerializer, SubscriptionUpdateSerializer, SearchSerializer, \
    SeasonSerializer, SubscriptionCreateSerializer, UserUpdateSerializer, \
    TrackSerializer, UserProfileSerializer
from constants import SUBSCRIPTION_FORGONE, SUBSCRIPTION_WATCHED, \
    SUBSCRIPTION_UNWATCHED, SUBSCRIPTION_WATCHING


class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = (ReadOnly,)


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner, IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH', ):
            return SubscriptionUpdateSerializer
        elif self.request.method in ('GET', ):
            return SubscriptionSerializer
        return SubscriptionCreateSerializer

    def get_queryset(self):
        return Subscription.objects.filter(~Q(status=SUBSCRIPTION_FORGONE) &
                                           Q(user=self.request.user))

    def pre_save(self, obj):
        obj.user = self.request.user

    # override `create` method
    def create(self, request, *args, **kwargs):
        aid = request.DATA.get('id')
        anime = Anime.objects.filter(aid=aid)
        if not anime:
            # Get the anime data from back_end
            anime_data = get_anime_detail(aid=aid)
            if not anime_data:
                raise APIException(detail='Anime not found')

            # convert the timestamp to `datetime` object, then save the object
            anime_data['updated_time'] = datetime.fromtimestamp(anime_data['updated_time'])
            _anime = AnimeSerializer(data=anime_data)
            if _anime.is_valid():
                anime = _anime.save()
            else:
                return Response(data={'error': _anime._errors}, status=status.HTTP_400_BAD_REQUEST)

            seasons = anime_data['season'] if anime_data else anime
            # Save the `season`
            for season in seasons:
                if not Season.objects.filter(season_id=season['season_id']):
                    season['anime'] = anime.id
                    _season = SeasonSerializer(data=season)
                    if _season.is_valid():
                        _season.save()
        else:
            anime = anime[0]

        instance = Subscription.objects.filter(Q(user=self.request.user) & Q(anime_id=anime.id))

        if not instance:
            Subscription.objects.create(anime=anime, user=self.request.user)
        else:
            instance = instance.first()
            if not instance.status == SUBSCRIPTION_FORGONE:
                raise APIException(detail='You had already add the anime to your subscriptions.')
            instance.status = SUBSCRIPTION_WATCHING
            instance.currently_watched = 0
            instance.save()

        return Response(data={'anime': anime.id}, status=status.HTTP_201_CREATED)

    # override `update` method
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.status == SUBSCRIPTION_FORGONE:
            raise APIException(detail='Detail not found')
        # `SUBSCRIPTION_FORGONE` status only can be marked when
        # the `DELETE` method been used
        request_data = dict(copy.deepcopy(request.data))
        if not status in (SUBSCRIPTION_WATCHED, SUBSCRIPTION_WATCHING):
            request_data['status'] = SUBSCRIPTION_WATCHING

        serializer = self.get_serializer(instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # TODO: if the anime don't have any season, then?
        # check the submitted `count` is valid or not
        currently_watched = int(request.data['currently_watched'])
        if instance.season:
            if (instance.season.count < currently_watched or currently_watched < 0):
                raise APIException(detail='The episode count is not valid')
        else:
            if instance.anime.episode < currently_watched:
                raise APIException(detail='The episode count is not valid')

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = SUBSCRIPTION_FORGONE
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SearchSerializer

    def get_queryset(self):
        keyword = self.request.GET.get('keyword', None)
        if not keyword:
            return []

        data = Anime.objects.filter(Q(name__contains=keyword) | Q(description__contains=keyword))
        return data if data else search(keyword)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSelf,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST', ):
            return UserCreateSerializer
        elif self.request.method in ('PUT', 'PATCH'):
            return UserUpdateSerializer
        else:
            return UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = UserSerializer if instance == request.user \
            else UserProfileSerializer
        serializer = serializer_class(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = UserCreateSerializer(data=request.DATA)
        if user.is_valid():
            if User.objects.filter(email__iexact=user.data['email']):
                raise APIException(detail='The email had been used.')
            User.objects.create_user(**user.data)
            return Response(user.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
