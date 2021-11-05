from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AbstractModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


