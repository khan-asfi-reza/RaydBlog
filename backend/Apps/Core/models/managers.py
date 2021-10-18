from django.db import models


class UserForeignKeyManager(models.Manager):
    """
    Must have a user foreign key / one to one field
    """

    # Returns only active
    def queryset_all(self, **kwargs):
        return self.filter(user__is_active=True, **kwargs).order_by("user_id")

    # Reduces Query time
    def queryset_all_with_users(self):
        return self.queryset_all().select_related("user")
