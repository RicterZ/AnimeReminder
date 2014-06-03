from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return False


class NoPermission(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsSelf(BasePermission):
    def has_permission(self, request, view):
        return not request.user == AnonymousUser()

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return not request.user == AnonymousUser()

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user