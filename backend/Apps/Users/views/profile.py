from django.http import Http404
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from Apps.Core.views.generics import CoreRetrieveUpdateAPIView, CreateAPI
from Apps.Users.models import Profile
from Apps.Users.models.profile import Follower
from Apps.Users.permissions.get_or_is_user import GetOrIsUserOwner
from Apps.Users.serializers.profiles import ProfileSerializer, UserProfileSerializer, FollowerSerializer, \
    FollowingSerializer, PerformFollowUnfollowSerializer


class UserProfileRetrieveUpdateView(CoreRetrieveUpdateAPIView):
    """
    PUT / PATCH / GET Method
    PUT Method request body
    {
        "user",
        "profile_picture",
        "bio",
        "website",
        "gender",
        "follower_status"
    }

    Response same as request body
    """
    permission_classes = [GetOrIsUserOwner]
    serializer_class = ProfileSerializer
    lookup_field = "user_id"
    queryset = Profile.objects.all()


class UserProfileListView(ListAPIView):
    """
        GET Method
        GET Method request response
        {
            "user",
            "profile_picture",
            "bio",
            "website",
            "gender",
            "follower_status"
        }
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.get_queryset()


class FollowerListView(ListAPIView):
    """
        GET Method
        GET Method request response
        {
            "followee"
            "follower"
        }
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer
    lookup_field = "followee_id"

    def get_queryset(self):
        followee_id = self.kwargs.get("followee_id")

        if followee_id:
            return Follower.objects.filter(followee=self.kwargs.get("followee_id"))

        return Http404


class FollowingListView(ListAPIView):
    """
    GET Method
    GET Method request response
    {
        "followee"
        "follower"
    }
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FollowingSerializer
    lookup_field = "follower_id"

    def get_queryset(self):
        followee_id = self.kwargs.get("follower_id")

        if followee_id:
            return Follower.objects.filter(followee=self.kwargs.get("follower_id"))

        return Http404


class FollowUnfollowCreateView(CreateAPI):
    """
    POST Method
    body
    {
        "followee",
        "follower",
        "action",
    }
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PerformFollowUnfollowSerializer


