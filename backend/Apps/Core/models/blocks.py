from django.db import models
from django.contrib.auth import get_user_model

from Apps.Core.models.abstract import AbstractModel
from Apps.Core.models.managers import UserForeignKeyManager
from Apps.Core.models.block_manager import ReactionManager
from utils.model_utils import file_location

User = get_user_model()

"""
Block Category
"""


class BlockCategory(AbstractModel):
    # Parent Category
    parent = models.ForeignKey(to="self",
                               on_delete=models.SET_NULL,
                               null=True,
                               verbose_name="Category Parent",
                               )
    # Category Name
    category_name = models.CharField(max_length=200, verbose_name="Category Name")

    def __str__(self):
        string = ""
        if self.parent is None:
            return self.category_name
        else:
            string = f"{str(self.parent)} > " + self.category_name + string

        return string

    class Meta:
        ordering = ["-id"]
        verbose_name = "Block Category"
        verbose_name_plural = "Block Categories"


"""
Block Post and Comment
"""


class BlockCommentAbstractModel(AbstractModel):
    # Text
    text = models.TextField(verbose_name="Block Content")
    # Reactions
    reactions = models.PositiveBigIntegerField(default=0, verbose_name="Block Reactions")
    # Object
    objects = UserForeignKeyManager()

    class Meta:
        abstract = True

    def increase_reactions(self):
        self.reactions += 1
        self.save()

    def decrease_reactions(self):
        self.reactions -= 1
        self.save()


class BlockPost(BlockCommentAbstractModel):
    # Owner / Author of the User
    user = models.ForeignKey(to=User,
                             on_delete=models.CASCADE,
                             verbose_name="Author")
    # Parent post
    parent = models.ForeignKey(to="self",
                               on_delete=models.SET_NULL,
                               null=True,
                               verbose_name="Parent Post",
                               )
    # Block Category
    block_category = models.ForeignKey(to=BlockCategory,
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "BlockPost"
        verbose_name_plural = "BlockPosts"

    # Check if post is shared or not
    @property
    def is_shared(self):
        return self.parent is not None

    def save(self, *args, **kwargs):
        if self.parent and self.parent.parent:
            self.parent = self.parent.parent

        super(BlockPost, self).save(*args, **kwargs)


class BlockPostImage(AbstractModel):
    # Owner User
    user = models.ForeignKey(to=User,
                             on_delete=models.CASCADE,
                             verbose_name="Block Post Image Author")
    # Parent Block Post
    block_post = models.ForeignKey(to=BlockPost,
                                   on_delete=models.CASCADE,
                                   verbose_name="Block Post")
    # Image
    image = models.ImageField(upload_to=file_location,
                              null=True, blank=True,
                              verbose_name="Block Post Image")


class BlockComment(BlockCommentAbstractModel):
    # User / Author
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Block Comment")
    # Parent Comment
    parent = models.ForeignKey(to="self",
                               on_delete=models.SET_NULL,
                               null=True,
                               verbose_name="Block Parent")
    # Post
    block_post = models.ForeignKey(to=BlockPost,
                                   on_delete=models.CASCADE,
                                   null=True,
                                   verbose_name="Block Post")

    @property
    def is_comment_reply(self):
        return self.parent is not None

    def save(self, *args, **kwargs):
        if self.parent and self.parent.parent:
            self.parent = self.parent.parent

        super(BlockComment, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created", ]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


"""
Block and Block Comment Reaction

Block Reaction Model

Block Content Comment Reaction Model

"""

REACTION_MAX_NUMBER = 3


class ReactionAbstractModel(AbstractModel):
    """
    0 - Null
    1 - Heart
    2 - Wow
    3 - Funny
    """
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


class BlockReaction(ReactionAbstractModel):
    # Parent Block Post
    block_post = models.ForeignKey(to=BlockPost,
                                   on_delete=models.CASCADE,
                                   verbose_name="Block Post")

    objects = ReactionManager("block_post")

    class Meta:
        ordering = ["-created", ]
        verbose_name = "Block Reaction"
        verbose_name_plural = "Block Reactions"


class BlockCommentReaction(ReactionAbstractModel):
    # Block Comment
    comment = models.ForeignKey(to=BlockComment,
                                on_delete=models.CASCADE,
                                verbose_name="Block Comment")

    objects = ReactionManager("comment")

    class Meta:
        ordering = ["-created", ]
        verbose_name = "Comment Reaction"
        verbose_name_plural = "Comment Reactions"
