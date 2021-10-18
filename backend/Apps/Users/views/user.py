from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView

from Apps.Users.serializers.users import UserDetailsSerializer, UserProfileShortSerializer, UserProfileDetailsSerializer

User = get_user_model()


class UserCreateView(CreateAPIView):
    """
    User Create View to create new users
    """
    serializer_class = UserDetailsSerializer


user_create_view = UserCreateView.as_view()


class UserProfileRetrieveView(RetrieveAPIView):
    """
    PUT / PATCH / GET Method
    PUT Method request body
    {
        "user",
        "profile": {
        "profile_picture",
        "bio",
        "website",
        "gender",
        "follower_status"
        }
    }

    Response same as request body
    """
    serializer_class = UserProfileDetailsSerializer
    lookup_field = "id"
    queryset = User.objects.all()


class UserProfileListView(ListAPIView):
    """
        GET Method
        GET Method request response
        {
            "user",
            "profile": {
            "profile_picture",
            "bio",
            "website",
            "gender",
            "follower_status"
            }
        }
    """
    serializer_class = UserProfileShortSerializer
    queryset = User.objects.all()
