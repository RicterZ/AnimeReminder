from django.db.models import Q
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from models import Anime, User, Subscription
from permission import NoPermission, IsOwner, IsSelf, ReadOnly
from serializers import AnimeSerializer, UserSerializer, SubscriptionSerializer
from back_end.parse_kankan import get_anime_detail, search_anime


class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = (IsAuthenticated,)
    #permission_classes = (NoPermission,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSelf,)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user

    def create(self, request, *args, **kwargs):
        aid = request.DATA.get('anime')
        if not Anime.objects.filter(aid=aid):
            anime_data = get_anime_detail(aid)
            if anime_data:
                Anime.objects.create(**anime_data)
        if Subscription.objects.filter(Q(user=self.request.user) & Q(anime_id=self.request.DATA['anime'])):
            return Response(data={"error": "You had already add the anime to your subscriptions."},
                            status=status.HTTP_400_BAD_REQUEST)
        # In fact, there should be checked in the serializer.py, at the `SubscriptionSerializer`'s validate method.
        return super(SubscriptionViewSet, self).create(request, *args, **kwargs)


class SearchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnimeSerializer

    def get_queryset(self):
        keyword = self.request.GET.get('name', None)
        if not keyword:
            return []

        data = Anime.objects.filter(Q(name__contains=keyword) | Q(bilibili_name__contains=keyword))
        return data if data else search_anime(keyword)
