from rest_framework import serializers
from Apps.Core.models import BlockPost, BlockReaction
from Apps.Core.models.blocks import REACTION_MAX_NUMBER, BlockComment
from Apps.Users.serializers.users import UserProfileShortSerializer


class BlockCreateEditSerializer(serializers.ModelSerializer):
    """
    Block Post Create and Edit Serializer
    """
    user: UserProfileShortSerializer = UserProfileShortSerializer(read_only=True)
    user_reaction: int = serializers.SerializerMethodField()

    def get_user_reaction(self, obj):
        # Request Context
        request = self.context.get("request", None)
        # If user is authenticated
        if request and request.user.is_authenticated:
            reaction_data = BlockReaction.objects.filter(
                block_post=obj,
                user=request.user
            )
            # Send Reaction Type if exist or 0
            if reaction_data.exists():
                return reaction_data.first().reaction_type
            else:
                return 0

    class Meta:
        model = BlockPost

        fields = ["id", "user", "parent", "text", "created", "updated", "block_category", "user_reaction", "reactions"]

        read_only_fields = ("id",
                            "created",
                            "updated",
                            "user",
                            "user_reaction",
                            "reactions"
                            )


class ParentReactionCreateSerializer(serializers.Serializer):
    """
    Parent Post Reaction Create Serializer
    """
    reaction_type = serializers.IntegerField(required=True)
    parent = serializers.IntegerField(required=True)
    reactions = serializers.IntegerField(read_only=True)
    parent_model = None

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        # Request Context
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            # Block Post
            block_post = BlockPost.objects.filter(id=validated_data.get("parent"))
            if not block_post.exists():
                raise serializers.ValidationError({
                    "block_post": "Invalid Block Post"
                })
            # Reaction Type
            reaction_type = validated_data.get("reaction_type")
            if reaction_type > REACTION_MAX_NUMBER:
                raise serializers.ValidationError({
                    "reaction_type": "Invalid Reaction"
                })
            # Reaction Type - 0 : Delete Reaction || Else Add or Edit Reaction
            reaction, number_of_reaction = BlockReaction.objects.create_reaction(
                block_post.first(),
                request.user,
                reaction_type
            )
            validated_data["reactions"] = number_of_reaction
            return validated_data

        else:
            raise serializers.ValidationError({
                "block_post": "Invalid Block Post"
            })


class BlockPostReactionCreateSerializer(ParentReactionCreateSerializer):
    """
        For Block Post
        Parent Block Post Reaction Create Serializer
    """
    parent_model = BlockPost

    def update(self, instance, validated_data):
        pass


class BlockCommentReactionCreateSerializer(ParentReactionCreateSerializer):
    """
        For Block Comment Post
        Parent Block Comment Post Reaction Create Serializer
    """
    parent_model = BlockComment

    def update(self, instance, validated_data):
        pass


class BlockReactionListSerializer(serializers.ModelSerializer):
    """
        User Reaction List Serializer
    """
    user: UserProfileShortSerializer = UserProfileShortSerializer(read_only=True)

    class Meta:
        model = BlockReaction
        fields = ["id", "block_post", "user", "reaction_type"]
