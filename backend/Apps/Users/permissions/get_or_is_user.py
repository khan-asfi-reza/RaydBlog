from rest_framework.permissions import BasePermission


class GetOrIsUserOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        elif request.method == "PUT" or request.method == "PATCH":
            return obj.user == request.user
