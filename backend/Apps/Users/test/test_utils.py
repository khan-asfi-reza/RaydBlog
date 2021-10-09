import datetime
import random

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from utils.model_utils import create_random_text, create_random_length_number, as_dict

user = get_user_model()

GLOBAL_TEST_PASSWORD = "TESTPASSWORD_@1011011"


# User Object Data

class UserObject:
    username = f"{create_random_text(20)}_{random.randrange(100)}"
    first_name = create_random_text(20)
    last_name = create_random_text(20)
    email = f"{create_random_text(10)}@email.com"
    phone_number = str(create_random_length_number())
    phone_number_ccode = "+880"
    password = GLOBAL_TEST_PASSWORD
    date_of_birth = datetime.date(day=12, month=12, year=2002)


# Create Test User
def create_test_user() -> (UserObject, type(get_user_model())):
    user_data = as_dict(UserObject)
    user_object, created = user.objects.get_or_new(**user_data)
    return UserObject, user_object


# Create Test User Profile
class ProfileObject:
    bio = "TEST BIO"
    gender = 1
    website = "www.example.com"


class APIAuthClient(APIClient):

    def __init__(self, **defaults):
        super().__init__(**defaults)
        self.user_object, self.user = create_test_user()
        self.__get_jwt_access_token()

    def __get_jwt_access_token(self):
        # Reverse URL
        url = reverse("jwt-obtain")
        # Response
        res = self.post(
            url, {"username": self.user_object.username,
                  "password": GLOBAL_TEST_PASSWORD}, format="json"
        )
        self.access_token = ""
        # Set Access Token
        if res.status_code == 200:

            self.access_token = res.data["access"]

        self.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

