from datetime import datetime
from django.core.files import File
from django.db import models
from django.contrib.auth import get_user_model

from utils.model_utils import file_location

User = get_user_model()

GENDER_CHOICE = [(1, "Male"), (2, "Female"), (3, "Prefer Not To Say"), (4, "Non Binary")]


class ProfileManager(models.Manager):
    def all(self):
        return self.filter(user__is_active=True).order_by("user_id")


class Profile(models.Model):
    # User
    user: User = models.OneToOneField(to=User, on_delete=models.CASCADE)
    # Profile Picture
    profile_picture: File = models.ImageField(upload_to=file_location,
                                              verbose_name="Profile Picture",
                                              null=True,
                                              blank=True)

    # Profile Bio
    bio: str = models.CharField(max_length=256, verbose_name="Bio", blank=True, default="")
    # Website
    website: str = models.CharField(max_length=256, verbose_name="Website", blank=True, default="")
    # Gender
    gender = models.IntegerField(
        choices=GENDER_CHOICE,
        blank=True,
        null=True
    )
    # Is profile complete
    profile_complete: bool = models.BooleanField(default=False)

    objects = ProfileManager()

    def __str__(self) -> str:
        return self.user.name

    class Meta:
        ordering = ("user_id",)


class UserFollowStatusManager(models.Manager):
    ACTION_TYPE = {
        "INCREMENT": 1,
        "DECREMENT": -1,
    }

    def __action_on_status(self, user_id: int, action_type: str, action_data: str) -> int:
        """

        :param user_id: User's ID(int)
        :param action_type: INCREMENT / DECREMENT
        :param action_data: FOLLOWER / FOLLOWING
        :return: Number of followers or followings
        """
        user_follow_status, created = self.get_or_create(user_id=user_id)
        # Increment or Decrement Follower and Following
        if action_data == "FOLLOWER":
            user_follow_status.follower += self.ACTION_TYPE[action_type]
        else:
            user_follow_status.following += self.ACTION_TYPE[action_type]
        # Save Data
        user_follow_status.save()

        # Return Data
        if action_data == "FOLLOWER":
            return user_follow_status.follower
        else:
            return user_follow_status.following

    def increment_follower(self, user_id: int) -> int:
        return self.__action_on_status(user_id, "INCREMENT", "FOLLOWER")

    def increment_following(self, user_id: int) -> int:
        return self.__action_on_status(user_id, "INCREMENT", "FOLLOWING")

    def decrement_follower(self, user_id: int) -> int:
        return self.__action_on_status(user_id, "DECREMENT", "FOLLOWER")

    def decrement_following(self, user_id: int) -> int:
        return self.__action_on_status(user_id, "DECREMENT", "FOLLOWING")


# User Following and Follower Status
class UserFollowStatus(models.Model):
    """
    Instead of Caching, we are using Database to store the numbers which will reduce the time than using
    objects.all.count() method

    user :- The Root user, who will have follower or have followings
    follower :- How many followers
    following :- How many followings

    """
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    follower = models.PositiveBigIntegerField(default=0)
    following = models.PositiveBigIntegerField(default=0)

    objects = UserFollowStatusManager()

    class Meta:
        verbose_name = "User Follow and Following Status"
        verbose_name_plural = "User Follow and Following Statuses"


# User Follower Map
class Follower(models.Model):
    """
        user :- The Root user, who will have follower or have followings
        follower :- The user who will follow the root user
    """
    followee = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="fl_map_followee")
    follower = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="fl_map_follower")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Follower List"
        verbose_name_plural = "User Followers List"
        unique_together = ["follower", "followee"]


def create_follow(followee_id: int, follower_id: int) -> tuple[int, int]:
    """
    Create Follow Relationship between Two Users
    :param followee_id: The user who will be followed
    :param follower_id: The User who will follow
    :return: tuple(follower_number, following_number)
             Following Number represents the number of the follower_id_user's followings
             Follower Number represents the number of the followee_id_user's followers
    """
    try:
        # Find Relationship following and follower
        follow_relationship = Follower.objects.filter(followee_id=followee_id, follower_id=follower_id)
        # If exists return True
        if follow_relationship.exists():
            return -1, -1
        # Else Create Relationship
        Follower.objects.create(followee_id=followee_id, follower_id=follower_id)
        # Following Number
        following_number = UserFollowStatus.objects.increment_following(follower_id)
        # Follower Number
        follower_number = UserFollowStatus.objects.increment_follower(followee_id)
        return follower_number, following_number

    except User.DoesNotExist:
        return -1, -1


def create_unfollow(followee_id: int, follower_id: int) -> tuple[int, int]:
    """
    Delete Follower Relationship
    :param followee_id: Whom to Unfollow
    :param follower_id: The person who will unfollow
    :return: tuple(follower_number, following_number)
             Following Number represents the number of the follower_id_user's followings
             Follower Number represents the number of the followee_id_user's followers
    """
    try:
        # Find Relationship following and follower
        follow_relationship = Follower.objects.filter(followee_id=followee_id, follower_id=follower_id)
        # If exists Delete and Return True
        follow_relationship.delete()
        # Following Number
        following_number = UserFollowStatus.objects.decrement_following(follower_id)
        # Follower Number
        follower_number = UserFollowStatus.objects.decrement_follower(followee_id)
        return follower_number, following_number

    except User.DoesNotExist:
        return -1, -1
