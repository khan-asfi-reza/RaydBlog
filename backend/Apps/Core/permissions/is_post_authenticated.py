from rest_framework.permissions import BasePermission


class IsPostAndAuthenticated(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return request.user.is_authenticated

        return True


class IsUserOwnerAndPut(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == "PUT" and obj.user == request.user


class IsUserOwnerAndAuthenticated(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return request.user.is_authenticated

        if request.method == "PUT":
            return request.user.is_authenticated and obj.user == request.user

        return True


class IsEditAuthenticatedOrTrue(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return False

        if request.method == "PUT" or request.method == "DELETE":
            return request.user.is_authenticated and obj.user == request.user

        return True
