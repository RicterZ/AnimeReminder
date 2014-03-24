from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from models import Anime, User, Subscription
from permission import NoPermission, IsOwner, IsSelf
from serializers import AnimeSerializer, UserSerializer, SubscriptionSerializer
from back_end.parse_kankan import get_kankan_anime_detail


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
        if not Anime.objects.filter(pk=aid):
            anime_data = get_kankan_anime_detail(aid)
            Anime.objects.create(**anime_data)
        return super(SubscriptionViewSet, self).create(request, *args, **kwargs)
