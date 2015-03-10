from datetime import datetime
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from models import Anime, Subscription, User, Season
from exceptions import RegisterException
from permission import IsOwnerOrReadOnly, ReadOnly, IsOwner, AnonymousUser, IsAuthenticated
from serializers import AnimeSerializer, SubscriptionSerializer, UserSerializer, \
    SubscriptionUpdateSerializer, SearchSerializer, SeasonSerializer, SubscriptionCreateSerializer
from back_end.bilibili import get_anime_detail, search


class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = (ReadOnly,)


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner, IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in ('PUT', ):
            return SubscriptionUpdateSerializer
        elif self.request.method in ('GET', ):
            return SubscriptionSerializer
        return SubscriptionCreateSerializer

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

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
                return Response(data={'error': 'Anime not found'}, status=status.HTTP_404_NOT_FOUND)

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

        if Subscription.objects.filter(Q(user=self.request.user) & Q(anime_id=anime.id)):
            return Response(data={'error': 'You had already add the anime to your subscriptions.'},
                            status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.create(anime=anime, user=self.request.user)
        return Response(data={'anime': anime.id}, status=status.HTTP_201_CREATED)

    # override `update` method
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # TODO: if the anime don't have any season, then?
        # check the submitted `count` is valid or not
        currently_read = int(request.data['currently_read'])
        if instance.season:
            if (instance.season.count < currently_read or currently_read < 0):
                return Response(data={'error': 'The episode count is not valid'})
        else:
            if instance.anime.episode < currently_read:
                return Response(data={'error': 'The episode count is not valid'})

        self.perform_update(serializer)
        return Response(serializer.data)


class SearchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SearchSerializer

    def get_queryset(self):
        keyword = self.request.GET.get('keyword', None)
        if not keyword:
            return []

        data = Anime.objects.filter(Q(name__contains=keyword) | Q(description__contains=keyword))
        return data if data else search(keyword)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.DATA)
        if serializer.is_valid():
            if User.objects.filter(email__iexact=serializer.data['email']).count() \
                    and serializer.data['email']:
                raise RegisterException('The email had been used.')
            if User.objects.filter(username__iexact=serializer.data['username']):
                raise RegisterException('The username had been used.')
            User.objects.create_user(username=serializer.data['username'],
                                              password=serializer.data['password'], email=serializer.data['email'])
            return Response({'status': 'Register a user successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

