from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from models import Anime, Subscription, User
from exceptions import RegisterException
from permission import IsOwnerOrReadOnly, ReadOnly, IsOwner, AnonymousUser, IsAuthenticated
from serializers import AnimeSerializer, SubscriptionSerializer, UserSerializer, \
    SubscriptionUpdateSerializer
from back_end.parse_kankan import get_anime_detail


class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    # for debug
    #permission_classes = (ReadOnly,)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsOwner, IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return SubscriptionUpdateSerializer
        return SubscriptionSerializer

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
        return data if data else ''


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
            return Response({"status": "Register a user successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

