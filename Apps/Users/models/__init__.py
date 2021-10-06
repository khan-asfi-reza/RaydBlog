from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.model_utils import generate_random_image
from .user import User
from .profile import Profile, GENDER_CHOICE


@receiver(post_save, sender=User)
def user_create_post_save(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def profile_post_save(sender, instance, created, **kwargs):
    if created:
        if not instance.profile_picture:
            # Get Gender Text
            gender = GENDER_CHOICE[instance.gender - 1][1].lower() if instance.gender else "RANDOM"
            img, filename = generate_random_image(gender, "image")
            # Save Image
            instance.profile_picture.save(filename, img)
            instance.save()
