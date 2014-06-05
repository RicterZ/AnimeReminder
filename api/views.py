from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from models import Anime, Subscription, UserExtension
from exceptions import RegisterException
from permission import IsOwnerOrReadOnly, ReadOnly, IsOwner, AnonymousUser, IsAuthenticated
from serializers import AnimeSerializer, SubscriptionSerializer, UserExtensionSerializer, UserExtensionCreateSerializer
from back_end.parse_kankan import get_anime_detail, search_anime


class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = (ReadOnly,)


class SubscriptionViewSet(viewsets.mixins.CreateModelMixin,
                          viewsets.mixins.DestroyModelMixin,
                          viewsets.mixins.RetrieveModelMixin,
                          viewsets.mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsOwner, IsAuthenticated,)

    def get_queryset(self):
        if self.request.user == AnonymousUser():
            return []
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


class UserExtensionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = UserExtension.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'GET'):
            return UserExtensionCreateSerializer
        return UserExtensionSerializer

    def pre_save(self, obj):
        if UserExtension.objects.filter(email=obj.email).count() and obj.email:
            raise RegisterException('The email had been used.')
        #super(UserExtensionViewSet, self).pre_save(obj=obj)