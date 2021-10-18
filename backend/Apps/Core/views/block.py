from Apps.Core.models import BlockPost
from Apps.Core.permissions.is_post_authenticated import IsPostAndAuthenticated
from Apps.Core.serializers.block import BlockCreateEditSerializer
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
