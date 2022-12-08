from rest_framework.permissions import BasePermission


class Dono(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.usuario == request.user or request.user.is_superuser

    def has_permission(self, request, view):
        return super().has_permission(request, view)

