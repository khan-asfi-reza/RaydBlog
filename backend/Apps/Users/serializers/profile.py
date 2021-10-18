from rest_framework import serializers

from Apps.Users.models.profile import UserFollowStatus, Profile


class UserFollowStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowStatus
        fields = ["follower", "following"]


class ProfileSerializer(serializers.ModelSerializer):
    """
        Profile Serializer is only for Profile Creation and Public Profile Viewing
    """
    class Meta:
        model = Profile
        fields = ["user", "profile_picture", "bio", "website", "gender", "reactions"]


class ProfilePictureSerializer(serializers.ModelSerializer):
    """
        For Profile Picture only
    """

    class Meta:
        model = Profile
        fields = ["user", "profile_picture"]