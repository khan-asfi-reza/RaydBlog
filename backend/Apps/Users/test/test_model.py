from django.urls import reverse
from rest_framework.test import APITestCase

from Apps.Users.models import Profile
from Apps.Users.models.profile import create_follow, create_unfollow
from Apps.Users.test.test_utils import create_test_user, ProfileObject, GLOBAL_TEST_PASSWORD, APIAuthClient, UserObject
from utils.model_utils import as_dict


class ModelTest(APITestCase):

    def test_user_create(self):
        user_object, user = create_test_user()
        # Test user
        self.assertEqual(user_object.username, user.username)
        self.assertEqual(user_object.first_name + ' ' + user_object.last_name, user.name)
        self.assertEqual(user_object.phone_number_ccode + user_object.phone_number, user.phone_number_full)
        self.assertEqual(user.check_password(GLOBAL_TEST_PASSWORD), True)

    def test_profile_create(self):
        user = create_test_user()[1]
        profile = Profile.objects.filter(
            user=user
        )
        profile.update(
            **as_dict(ProfileObject)
        )
        # Test
        self.assertEqual(ProfileObject.website, profile.first().website)
        self.assertEqual(ProfileObject.bio, profile.first().bio)
        self.assertEqual(ProfileObject.gender, profile.first().gender)

    def test_user_create_api(self):
        url = reverse("user-create")
        user_data = as_dict(UserObject)
        user_data["password"] = GLOBAL_TEST_PASSWORD
        res = self.client.post(
            url,
            user_data
            , format="json"
        )

        self.assertEqual(res.status_code, 201)

        dup_res = self.client.post(
            url,
            user_data
            , format="json"
        )

        self.assertEqual(dup_res.status_code, 400)


class AuthTestCase(APITestCase):
    client_class: APIAuthClient = APIAuthClient

    def test_change_password(self):
        url = reverse("password-change")
        res = self.client.post(
            url, {
                "old_password": GLOBAL_TEST_PASSWORD,
                "new_password": GLOBAL_TEST_PASSWORD + "_new"
            }, format="json"
        )

        self.assertEqual(res.status_code, 201)

    def test_reset_password_with_username(self):
        # Password Reset Request
        url = reverse("password-forget")
        res = self.client.post(
            url,
            {
                "username": self.client.user.username
            }
        )
        self.assertEqual(res.status_code, 201)
        unique_code = res.data["json_data"]

        # Password validation
        url = reverse("password-validate-reset")
        res = self.client.post(url,
                               {
                                   "unique_code": unique_code
                               })
        self.assertEqual(res.status_code, 201)
        # Reset Password
        url = reverse("password-reset")
        res = self.client.post(
            url,
            {
                "unique_code": unique_code,
                "new_password": "NEW_PASSWORD_123"
            }
        )
        self.assertEqual(res.status_code, 201)

    def test_reset_password_with_email(self):
        url = reverse("password-forget")
        res = self.client.post(
            url,
            {
                "username": self.client.user.email
            }
        )
        self.assertEqual(res.status_code, 201)


class TestFollow(APITestCase):

    def test_user_follow_unfollow(self):
        user_1_obj, user_1 = create_test_user()
        user_2_obj, user_2 = create_test_user()
        # Test Functions
        follow_status = create_follow(user_1.id, user_2.id)
        self.assertEqual(follow_status[0], 1)
        self.assertEqual(follow_status[1], 1)
        # Test
        unfollow_status = create_unfollow(user_1.id, user_2.id)
        self.assertEqual(unfollow_status[0], 0)
        self.assertEqual(unfollow_status[1], 0)

    def test_user_profile_get_permission(self):
        # Test User Profile Get Expect Unauthorized
        user_1_obj, user_1 = create_test_user()
        url = reverse("profile-get", kwargs={"id": user_1.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_user_profile_edit_permission(self):
        # Test Edit Profile Except Unauthorized
        user_1_obj, user_1 = create_test_user()
        url = reverse("profile-edit", kwargs={"user_id": user_1.id})
        res = self.client.put(
            url,
            {
                "website": "NEW WEBSITE LINK"
            }
        )
        self.assertEqual(res.status_code, 401)


class TestUserProfile(APITestCase):
    client_class: APIAuthClient = APIAuthClient

    def test_user_get(self):
        # Test User To Get Profile
        user_obj, user = create_test_user()
        url = reverse("profile-get", kwargs={"id": user.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_user_profile_edit(self):
        # Test User to edit his profile
        user_obj, user = create_test_user()
        url = reverse("profile-edit", kwargs={"user_id": user.id})
        res = self.client.put(
            url,
            {
                "website": "NEW WEBSITE LINK"
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_user_profile_list(self):
        for i in range(100):
            create_test_user()

        url = reverse("profile-list")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_follow_unfollow(self):

        user_2 = create_test_user()[1]
        url = reverse("follow-unfollow")
        res = self.client.post(
            url,
            {
                "follower": self.client.user.id,
                "followee": user_2.id,
                "action": 1
            }

        )
        self.assertEqual(res.status_code, 201)
        url = reverse("follower-list", kwargs={"followee_id": user_2.id})
        res = self.client.get(
            url
        )
        self.assertEqual(res.status_code, 200)




