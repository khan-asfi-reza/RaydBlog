from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from Apps.Core.permissions.is_post_authenticated import IsUserOwnerAndPut
from Apps.Core.views.generics import CreateAPI, CoreUpdateAPIView
from Apps.Users.models.profile import Follower, Profile
from Apps.Users.serializers.follower import FollowerSerializer, \
    FollowingSerializer, PerformFollowUnfollowSerializer
from Apps.Users.serializers.profile import ProfileSerializer


class ProfileUpdateView(CoreUpdateAPIView):
    """
        PUT Method
        PUT Method request body
        {

        }
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsUserOwnerAndPut]
    lookup_field = "user_id"
    queryset = Profile.objects.queryset_all()


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
            return Follower.objects.filter(followee=self.kwargs.get("followee_id"),
                                           follower__is_active=True).order_by("id")

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
        follower_id = self.kwargs.get("follower_id")

        if follower_id:
            return Follower.objects.filter(follower=self.kwargs.get("follower_id"),
                                           followee__is_active=True).order_by("id")

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
