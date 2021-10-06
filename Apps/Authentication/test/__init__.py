from django.urls import reverse
from rest_framework.test import APITestCase
from Apps.Users.test.test_utils import create_test_user, GLOBAL_TEST_PASSWORD


class AuthenticationTestCase(APITestCase):
    def test_jwt_token(self):
        user_object, user = create_test_user()
        url = reverse("jwt-obtain")
        res = self.client.post(
            url, {"username": user_object.username, "password": GLOBAL_TEST_PASSWORD}, format="json"
        )
        self.assertEqual(res.status_code, 200)

        data = res.data

        url = reverse("jwt-refresh")
        res = self.client.post(url, {
            "refresh": data["refresh"]
        })
        self.assertEqual(res.status_code, 200)

    def test_jwt_with_email(self):
        user_object, user = create_test_user()
        url = reverse("jwt-obtain")
        res = self.client.post(
            url, {"username": user_object.email, "password": GLOBAL_TEST_PASSWORD}, format="json"
        )
        self.assertEqual(res.status_code, 200)