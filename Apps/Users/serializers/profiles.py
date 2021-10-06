from django.contrib.auth import get_user_model
from rest_framework import serializers
from Apps.Users.models.profile import Profile, UserFollowStatus, Follower, create_follow, create_unfollow
from Apps.Users.serializers.users import UserRetrieveSerializer

User = get_user_model()

FOLLOW_ACTION = 1
UNFOLLOW_ACTION = 1


class UserFollowStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowStatus
        fields = ["user", "follower", "following"]


class ProfileSerializer(serializers.ModelSerializer):
    """
        Profile Serializer is only for Profile Creation and Public Profile Viewing
    """
    follower_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ["user", "profile_picture", "bio", "website", "gender", "follower_status"]

    @staticmethod
    def get_follower_status(obj):
        try:
            return UserFollowStatusSerializer(instance=UserFollowStatus.objects.get(user=obj.user))
        except UserFollowStatus.DoesNotExist:
            return {}


class UserProfileSerializer(serializers.ModelSerializer):
    """
        For User and Profile Serializer
    """
    user = UserRetrieveSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["user", "profile_picture", "profile_complete"]


class ProfilePictureSerializer(serializers.ModelSerializer):
    """
        For Profile Picture only
    """
    user_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ["profile_picture", "user_id"]

    @staticmethod
    def get_user_id(obj):
        return obj.user.id


class FollowerSerializer(serializers.ModelSerializer):
    """
    User's Followers list
    """
    follower = UserProfileSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ["follower", "followee", "id"]


class FollowingSerializer(serializers.ModelSerializer):
    """
    User's Following List
    """
    followee = UserProfileSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ["follower", "followee", "id"]


class PerformFollowUnfollowSerializer(serializers.Serializer):
    """
    Serializer that will perform follow or unfollow action
    """

    # ACTION = {
    #     1: "FOLLOW",
    #     2: "UNFOLLOW"
    # }

    # Follower Id
    follower = serializers.IntegerField(required=True)
    # Followee Id
    followee = serializers.IntegerField(required=True)
    # Unfollow / Follow
    action = serializers.IntegerField(required=True)

    class Meta:
        model = Follower
        fields = ["follower", "followee"]

    def validate(self, attrs):
        # Validate
        follower = attrs.get("follower", None)
        followee = attrs.get("followee", None)
        action = attrs.get("action", None)
        if followee and follower and action:
            # Validate if user exists
            try:
                # Check User
                follower_user = User.objects.get(id=follower)
                User.objects.get(id=followee)
                request = self.context.get("request")
                if follower_user != request.user:
                    raise serializers.ValidationError(
                        {
                            "follower": "Invalid User, Authorization Error"
                        }
                    )
                # Check Action
                if action == FOLLOW_ACTION or action == UNFOLLOW_ACTION:
                    return attrs
                # Raise Validation if invalid action token
                raise serializers.ValidationError(
                    {
                        "action": "Invalid Action"
                    }
                )
            # Else Raise Error
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    "error": "User does not exist"
                })
        raise serializers.ValidationError({
            "error": "User does not exist"
        })

    def create(self, validated_data):
        # Get Validated Data
        follower = validated_data.get("follower", None)
        followee = validated_data.get("followee", None)
        action = validated_data.get("action", None)

        follower_number = following_number = 0

        if followee and follower and action:
            # If Action == 1 Create Follow
            if action == FOLLOW_ACTION:
                # Number of followers for the person who is being followed,
                # Follower Number -> Followee s Follower Number
                # Following Number -> Follower's Following Number
                follower_number, following_number = create_follow(followee, follower)
            # If Action == 2 Create Unfollow
            elif action == UNFOLLOW_ACTION:
                follower_number, following_number = create_unfollow(followee, follower)

            return {
                "followers": follower_number,
                "following_number": following_number
            }

    def update(self, instance, validated_data):
        raise NotImplementedError()
