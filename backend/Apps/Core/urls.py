from django.urls import path

from Apps.Core.views.block import block_create_list_view, block_retrieve_edit_delete_view, \
    block_reaction_create_api_view, block_reaction_list_api_view, block_comment_list_parents_create_api_view, \
    block_comment_child_list_api, block_comment_rud_api_view

urlpatterns = [
    path("block/", block_create_list_view, name="block-create"),
    path("block/<int:id>", block_retrieve_edit_delete_view, name="block-edit-retrieve-delete"),
    path("block-reaction/", block_reaction_create_api_view, name="block-reaction-create"),
    path("block-reaction/<int:block_post>", block_reaction_list_api_view, name="block-reaction-list"),
    path("block-comment/<int:block_post>/", block_comment_list_parents_create_api_view, name="block-comment-parent-create-list"),
    path("block-comment-child/<int:parent>/", block_comment_child_list_api, name="block-comment-child"),
    path("block-comment/<int:id>/", block_comment_rud_api_view, name="block-comment-rud")
]