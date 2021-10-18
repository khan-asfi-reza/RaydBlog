from rest_framework import serializers

from Apps.Core.models import BlockPost
from Apps.Users.serializers.users import UserProfileShortSerializer


class BlockCreateEditSerializer(serializers.ModelSerializer):
    """
    Block Post Create and Edit Serializer
    """
    user = UserProfileShortSerializer(read_only=True)

    class Meta:
        model = BlockPost
        fields = ["id", "user", "parent", "text", "created", "updated", "block_category"]
        read_only_fields = ("id", "created", "updated", "user",)
