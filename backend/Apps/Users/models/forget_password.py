# Forget Email
import datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.crypto import get_random_string

User = get_user_model()


def get_expiration_time():
    return timezone.now() + timedelta(hours=1)


class ForgetPasswordConsts:
    # Maximum Request Send Limit within a wait time limit
    MAXIMUM_REQUEST_SENT_THRESHOLD = 6
    # Wait Time for Maximum Request Send Limit in Minute
    MAXIMUM_REQUEST_SENT_WAIT_TIME = 20
    # Forget Password Email Template
    FORGET_PASSWORD_EMAIL_TEMPLATE = "forget_password.html"


class ForgetPasswordManager(models.Manager):

    def create_or_reset(self, user_query_data):
        user_obj = User.objects.filter(**user_query_data)
        if user_obj.exists():
            query_data, created = self.get_or_create(user=user_obj.first())
            """
            # Query Data Request Sent Validation
            # Check if Client has sent request more than or equal REQUEST SENT THRESHOLD
            """
            has_threshold_passed = query_data.request_sent >= ForgetPasswordConsts.MAXIMUM_REQUEST_SENT_THRESHOLD
            """
            Check if Forget Password Initialization has increased by MAXIMUM_REQUEST_SENT_WAIT_TIME
            """
            time_delta = timezone.timedelta(minutes=ForgetPasswordConsts.MAXIMUM_REQUEST_SENT_WAIT_TIME)
            has_time_passed = timezone.now() > query_data.time_stamp + time_delta
            """
            If Client has passed the maximum request sent threshold and initial time has increased by wait time
            Client can send else client can't send request
            """
            can_request_with_threshold = has_time_passed and has_threshold_passed
            if not has_threshold_passed or can_request_with_threshold:
                # Set Expiration Time to initial time + 1 hour
                query_data.expiration_time = timezone.now() + datetime.timedelta(hours=1)
                # Sent Request Save
                if query_data.request_sent >= ForgetPasswordConsts.MAXIMUM_REQUEST_SENT_THRESHOLD:
                    # Reset the request sent
                    query_data.request_sent = 1
                else:
                    query_data.request_sent += 1
                # Reset Link
                query_data.unique_link = get_random_string(30)
                # Save Object
                query_data.save()
                # Send Email
                return query_data, {}
            else:
                return None, {"error": ["Too many request sent, please wait another 20 minutes"]}

        return None, {"user": ["User with this data doesn't exist"]}


class ForgetPassword(models.Model):
    # User
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    # Unique Link
    unique_link = models.CharField(max_length=30, blank=True, null=True)
    # Creation Time
    time_stamp = models.DateTimeField(auto_now=True)
    # Expiration Time
    expiration_time = models.DateTimeField(default=get_expiration_time)
    # Changed
    changed = models.BooleanField(default=False)
    # Request Sent
    request_sent = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}"

    objects = ForgetPasswordManager()
