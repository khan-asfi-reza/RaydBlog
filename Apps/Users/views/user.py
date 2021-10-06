from Apps.Users.serializers.users import UserOnlySerializer
from rest_framework.generics import CreateAPIView


class UserCreateView(CreateAPIView):
    """
    User Create View to create new users
    """
    serializer_class = UserOnlySerializer


user_create_view = UserCreateView.as_view()


class UserDeactivateView():
    pass