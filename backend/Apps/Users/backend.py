from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth import get_user_model

from utils.model_utils import is_email

UserModel = get_user_model()


class UserAuthenticateBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check the token and return a user.

        if username is None or password is None:
            return
        try:
            IS_EMAIL = is_email(username)
            if IS_EMAIL:
                user = UserModel.objects.get(email=username)
            else:
                user = UserModel.objects.get(username=username)

        except UserModel.DoesNotExist:
            return
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
