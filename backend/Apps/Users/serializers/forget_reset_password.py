# Change Password Serializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
import json

from Main.env import IS_PROD
from Apps.Core.mail import SendEmail
from Apps.Users.models.forget_password import ForgetPassword, ForgetPasswordConsts
from utils.crypto import encrypt, decrypt
from utils.model_utils import check_email

User = get_user_model()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True,
                                         style={'input_type': 'password'},
                                         trim_whitespace=False)
    new_password = serializers.CharField(required=True,
                                         style={'input_type': 'password'},
                                         trim_whitespace=False)

    # Validates OLD password
    def validate(self, attrs):
        request = self.context.get('request')
        old_password = attrs.get('old_password')
        if not request.user.check_password(old_password):
            raise serializers.ValidationError({"error": ["Old password is wrong"]})
        return attrs

    # Create new password
    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data.get('new_password'))
        user.save()
        return {
            "msg": 1,
            "text": "Password successfully changed"
        }

    def update(self, instance, validated_data):
        raise NotImplementedError


class ResetPasswordLinkGenerateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

    # Validate
    def validate(self, attrs):
        # Query Parameter
        query_data = {

        }
        # User Data : Email / Username
        user_data = attrs.get("username", "")
        if user_data:
            # Check if email
            if check_email(user_data):
                query_data["email"] = user_data
            else:
                # Check if username
                query_data["username"] = user_data

            # Get Forget Password Object
            forget_pass_query, error_msg = ForgetPassword.objects.create_or_reset(query_data)

            # Raise Error
            if not forget_pass_query:
                raise serializers.ValidationError(error_msg)

            # Get Object
            attrs["forget_pass_query"] = forget_pass_query
            return attrs

        raise serializers.ValidationError({"user_data": "Invalid"})

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        # Get Object
        forget_pass_object = validated_data.get("forget_pass_query")

        # Create a encrypted unique identity to validate
        unique_link = {
            "unique_link": forget_pass_object.unique_link,
            "id": forget_pass_object.id
        }

        # Create Json object
        json_obj = json.dumps(unique_link)

        encrypted_json_obj = encrypt(json_obj)
        # Send Mail
        SendEmail().send_custom_context_html_email(
            template=ForgetPasswordConsts.FORGET_PASSWORD_EMAIL_TEMPLATE,
            subject="Main Password Reset",
            to=[forget_pass_object.user.email],
            body=encrypted_json_obj
        )
        # User Email as Secret
        email = forget_pass_object.user.email
        secret_email = email[0:4] + "*" * (len(email.split('@')[0]) - 3) + f"@{email.split('@')[1]}"
        # For Testing Purpose
        if IS_PROD == 0:
            return {
                "msg": 1,
                "secret_email": secret_email,
                "json_data": encrypted_json_obj,
            }
        return {
            "msg": 1,
            "secret_email": secret_email
        }


def check_valid_rest_code(reset_link, return_user=False):
    # Validate Unique Code and password
    if reset_link:
        # Decrypt Unique Reset Link
        unique_code_json = decrypt(reset_link)
        # Load Json
        unique_code = json.loads(unique_code_json)
        # Filter | Query
        forget_pass_object = ForgetPassword.objects.filter(id=unique_code["id"])
        # Validity Checker
        if forget_pass_object.exists():
            if forget_pass_object.first().unique_link == unique_code["unique_link"]:
                if return_user:
                    return forget_pass_object.first().user, forget_pass_object.first()

                return True

        return False


class ValidateUniqueLink(serializers.Serializer):
    unique_code = serializers.CharField(required=True)

    def validate(self, attrs):
        # Get Field Data
        unique_code = attrs.get("unique_code", "")

        if unique_code:
            res = check_valid_rest_code(unique_code)
            if res:
                attrs["response"] = res
                return attrs
            raise serializers.ValidationError({"error": "Invalid Code"})

        raise serializers.ValidationError({
            "unique_code": "Invalid Code"
        })

    def create(self, validated_data):
        return {
            "response": validated_data["response"],
            "msg": 1,
        }

    def update(self, instance, validated_data):
        raise NotImplementedError


class ResetPassword(serializers.Serializer):
    new_password = serializers.CharField(required=True,
                                         style={'input_type': 'password'},
                                         trim_whitespace=False)
    unique_code = serializers.CharField(required=True)

    def validate(self, attrs):
        # Get Field Data
        unique_code = attrs.get("unique_code", "")
        new_password = attrs.get("new_password", "")

        # Validate Unique Code and password
        if unique_code and new_password:
            user_data, fp_data = check_valid_rest_code(unique_code, True)
            if user_data:
                attrs["user"] = user_data
                attrs["fp_data"] = fp_data
                return attrs

            raise serializers.ValidationError({"error": "Invalid Code"})

        raise serializers.ValidationError({
            "new_password": "Invalid Password",
            "unique_code": "Invalid Code"
        })

    def create(self, validated_data):
        user = validated_data["user"]
        password = validated_data["new_password"]
        fp_data = validated_data["fp_data"]
        user.set_password(password)
        user.save()
        fp_data.delete()
        return {"msg": 1, "text": "User Password successfully changed"}

    def update(self, instance, validated_data):
        raise NotImplementedError()
