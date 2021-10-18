from asgiref.sync import sync_to_async
from django.db import models


class ReactionManager(models.Manager):

    def __init__(self, parent_field):
        self.parent_field = parent_field
        super().__init__()

    # Add Reaction
    def add_reaction(self, parent, user, reaction):
        from Apps.Users.models import Profile
        query_params = {
            self.parent_field: parent,
            "user": user
        }
        reaction_obj, created = self.get_or_create(**query_params)
        # Create Reaction
        reaction_obj.reaction_type = reaction
        # Save Reaction
        reaction_obj.save()
        # Increase Profile Reactions
        sync_to_async(Profile.objects.increase_reactions(user))
        # Increase Post Reactions
        sync_to_async(parent.increase_reactions())
        return reaction_obj

    # Delete Reaction
    def delete_reaction(self, parent, user, ):
        from Apps.Users.models import Profile
        # Delete Reaction Object
        query_params = {
            self.parent_field: parent,
            "user": user
        }
        self.filter(**query_params).delete()
        # Decrease Profile Reactions
        sync_to_async(Profile.objects.decrease_reactions(user))
        # Decrease Post Reactions
        sync_to_async(parent.decrease_reactions())
