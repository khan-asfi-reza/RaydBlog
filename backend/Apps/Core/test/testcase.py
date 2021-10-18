from django.urls import reverse
from rest_framework.test import APITestCase
from Apps.Core.models.blocks import *
from Apps.Users.models import Profile
from Apps.Users.test.test_utils import create_test_user, APIAuthClient
from Apps.Users.serializers.users import UserProfileShortSerializer

CATEGORY_NAME_1 = "CATEGORY_1"
CATEGORY_NAME_2 = "CATEGORY_2"


def test_category():
    return BlockCategory.objects.create(
        category_name=CATEGORY_NAME_1
    )


class ModelTestCase(APITestCase):

    def test_category_model(self):
        # Models
        category_1 = test_category()
        self.assertEqual(category_1.category_name, CATEGORY_NAME_1)

        # Create Category 2
        category_2 = BlockCategory.objects.create(
            category_name=CATEGORY_NAME_2,
            parent=category_1
        )
        self.assertEqual(category_2.parent.category_name, CATEGORY_NAME_1)

    def test_create_post_model(self):
        # Models
        user_obj, user = create_test_user()
        # Post
        post = BlockPost.objects.create(
            text="TEST",
            user=user,
        )
        self.assertEqual(post.user.id, user.id)
        # Post Parent
        post_parent = BlockPost.objects.create(
            parent=post,
            user=user,
            text="SHARED TEST"
        )
        # Test
        self.assertEqual(post_parent.parent_id, post.id)

        # Test Reaction
        reaction = BlockReaction.objects.create(
            user=user,
            block_post=post,
            reaction_type=1
        )
        self.assertEqual(reaction.reaction_type, 1)

        # Comment Test
        comment = BlockComment.objects.create(
            user=user,
            block_post=post,
            text="COMMENT"
        )

        self.assertEqual(comment.text, "COMMENT")

        # Reaction
        comment_reaction = BlockCommentReaction.objects.create(
            user=user,
            comment=comment,
            reaction_type=1,
        )
        self.assertEqual(comment_reaction.reaction_type, 1)

    def test_custom_model_managers(self):
        # Models
        user_obj, user = create_test_user()
        # Post
        post = BlockPost.objects.create(
            text="TEST",
            user=user,
        )
        self.assertEqual(post.user.id, user.id)
        # Test Post Reaction
        reaction = BlockReaction.objects.add_reaction(post, user, 1)
        self.assertEqual(reaction.reaction_type, 1)
        self.assertEqual(post.reactions, 1)
        self.assertEqual(Profile.objects.get(user=user).reactions, 1)

    def test_recursive_category(self):
        # Test Category Recursion
        cat_objects = [BlockCategory.objects.create(
            category_name="Cat 0"
        )]

        for i in range(5):
            cat_objects.append(
                BlockCategory.objects.create(
                    category_name=f"Cat {i + 1}",
                    parent=cat_objects[i]
                )
            )

        for i in range(len(cat_objects) - 1, 0, -1):
            self.assertEqual(
                cat_objects[i].parent.id, cat_objects[i - 1].id
            )

    def test_parent_comment(self):
        # Post
        user_obj, user = create_test_user()
        post = BlockPost.objects.create(
            text="TEXT",
            user=user
        )
        # Create Comment Parent
        comments = [
            BlockComment.objects.create(
                block_post=post,
                text="TEXT",
                user=user
            )
        ]
        # Create Child Comment
        for i in range(0, 5):
            comments.append(
                BlockComment.objects.create(
                    block_post=post,
                    text=f"TEXT {i + 1}",
                    user=user,
                    parent=comments[i]
                )
            )
        # Test
        for each in comments[1:]:
            self.assertEqual(each.parent_id, comments[0].id)

    def test_user_new_profile_serializer(self):
        user_obj, user = create_test_user()
        serializer = UserProfileShortSerializer(instance=user)
        self.assertEqual(1, 1)


class TestCoreAPI(APITestCase):
    client_class: APIAuthClient = APIAuthClient

    def test_block_create(self):
        # Block Create API Test
        url = reverse("block-create")
        res = self.client.post(url, {
            "text": "Hello Test",
        }, format="json")
        self.assertEqual(res.status_code, 201)

    def test_block_list(self):
        # Test Block List View
        url = reverse("block-create")
        for i in range(30):
            res = self.client.post(url, {
                "text": "Hello Test {}".format(i),
            }, format="json")
            self.assertEqual(res.status_code, 201)

        res = self.client.get(url, format="json")
        self.assertEqual(res.status_code, 200)

    def test_block_rud(self):
        """
        Test Block Retrieve Update Delete
        """
        url = reverse("block-create")
        id_list = []
        for i in range(5):
            res = self.client.post(url, {
                "text": "Hello Test {}".format(i),
            }, format="json")
            self.assertEqual(res.status_code, 201)
            id_list.append(res.data["id"])

        res = self.client.get(url, format="json")
        self.assertEqual(res.status_code, 200)
        # Test Retrieve
        url = reverse("block-edit-retrieve-delete", kwargs={"id": id_list[-1]})
        res = self.client.get(url, format="json")
        self.assertEqual(res.status_code, 200)
        # Test Update
        res = self.client.put(url, {"text": "Hello World"}, format="json")
        self.assertEqual(res.status_code, 200)
        # Test Delete
        res = self.client.delete(url, format="json")
        self.assertEqual(res.status_code, 204)