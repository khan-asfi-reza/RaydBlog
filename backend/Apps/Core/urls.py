from django.urls import path

from Apps.Core.views.block import block_create_list_view, block_retrieve_edit_delete_view, \
    block_reaction_create_api_view, block_reaction_list_api_view

urlpatterns = [
    path("block/", block_create_list_view, name="block-create"),
    path("block/<int:id>", block_retrieve_edit_delete_view, name="block-edit-retrieve-delete"),
    path("block-reaction/", block_reaction_create_api_view, name="block-reaction-create"),
    path("block-reaction/<int:block_post>", block_reaction_list_api_view, name="block-reaction-list"),
]