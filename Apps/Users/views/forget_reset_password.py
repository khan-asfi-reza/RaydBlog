from rest_framework.permissions import IsAuthenticated

from Apps.Core.views.generics import CreateAPI
from Apps.Users.serializers.forget_reset_password import PasswordChangeSerializer, \
    ResetPasswordLinkGenerateSerializer, \
    ValidateUniqueLink, ResetPassword


class ChangePasswordAPI(CreateAPI):
    # Change Password
    serializer_class = PasswordChangeSerializer
    # Authentication Class
    permission_classes = [IsAuthenticated]


class ResetPasswordRequestAPI(CreateAPI):
    # Reset Password
    serializer_class = ResetPasswordLinkGenerateSerializer


class ResetPasswordLinkVerificationAPI(CreateAPI):
    # Validity Checker
    serializer_class = ValidateUniqueLink


class ResetPasswordAPI(CreateAPI):
    # Reset Password
    serializer_class = ResetPassword
