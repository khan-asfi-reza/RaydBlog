from django.db import models
from django.contrib.auth import get_user_model

from Apps.Core.models.managers import UserForeignKeyManager

User = get_user_model()


class AbstractModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ReactionAbstractModel(AbstractModel):
    REACTION_TYPE = [
        (
            1, "Heart"
        ),
        (
            2, "Wow"
        ),
        (
            3, "Funny"
        )
    ]
    # User / Author
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Reactor")
    # Reaction Type
    reaction_type = models.IntegerField(choices=REACTION_TYPE, default=1)

    objects = UserForeignKeyManager()

    class Meta:
        abstract = True

        ordering = ["-created"]
