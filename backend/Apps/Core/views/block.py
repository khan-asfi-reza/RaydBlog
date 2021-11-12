from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from Apps.Core.models import BlockPost, BlockReaction, BlockComment
from Apps.Core.permissions.is_post_authenticated import IsPostAndAuthenticated
from Apps.Core.serializers.block import BlockCreateEditSerializer, ParentReactionCreateSerializer, \
    BlockReactionListSerializer, BlockCommentSerializer
from Apps.Core.views.generics import UserCreateListAPIView, UserRetrieveUpdateDeleteAPIView


class BlockCreateListAPI(UserCreateListAPIView):
    """
    Block Create View
    """
    permission_classes = [IsPostAndAuthenticated]
    serializer_class = BlockCreateEditSerializer
    queryset = BlockPost.objects.get_queryset()


block_create_list_view = BlockCreateListAPI.as_view()


class BlockUpdateRetrieveDeleteAPI(UserRetrieveUpdateDeleteAPIView):
    """
    Block Update, Retrieve, Delete View
    """
    serializer_class = BlockCreateEditSerializer
    queryset = BlockPost.objects.get_queryset()
    lookup_field = "id"


block_retrieve_edit_delete_view = BlockUpdateRetrieveDeleteAPI.as_view()


class BlockReactionCreateAPI(CreateAPIView):
    """
    Create Reaction Of a Post
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ParentReactionCreateSerializer
    queryset = BlockReaction.objects.get_queryset()


block_reaction_create_api_view = BlockReactionCreateAPI.as_view()


class BlockReactionListAPI(ListAPIView):
    """
    List of Reactions
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BlockReactionListSerializer
    lookup_field = "block_post"

    def get_queryset(self):
        return BlockReaction.objects.filter(block_post=self.kwargs.get("block_post"))


block_reaction_list_api_view = BlockReactionListAPI.as_view()


class BlockCommentListParentsCreateAPI(UserCreateListAPIView):
    """
    Block Comment List Create [Only Parents List]
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BlockCommentSerializer
    queryset = BlockComment.objects.filter(parent=None)
    lookup_field = "block_post"


block_comment_list_parents_create_api_view = BlockCommentListParentsCreateAPI.as_view()


class BlockCommentChildListAPI(ListAPIView):
    """
    Block Comment List Child List
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BlockCommentSerializer
    lookup_field = "parent"

    def get_queryset(self):
        return BlockComment.objects.filter(parent=self.kwargs.get("parent"))


block_comment_child_list_api = BlockCommentChildListAPI.as_view()


class BlockCommentUpdateDeleteAPI(UserRetrieveUpdateDeleteAPIView):
    """
        Block Update, Retrieve, Delete View
    """
    serializer_class = BlockCommentSerializer
    queryset = BlockComment.objects.get_queryset()
    lookup_field = "id"


block_comment_rud_api_view = BlockCommentUpdateDeleteAPI.as_view()
