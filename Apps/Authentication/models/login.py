import uuid

from django.db import models

from django.contrib.auth import get_user_model

from utils.base import get_client_ip
from utils.crypto import encrypt, decrypt

User = get_user_model()

DEVICE_OS_TYPE = [
    (1, "iOS"),
    (2, "Android"),
    (3, "BlackBerry Tablet OS"),
    (4, "Windows Phone"),
    (5, "Windows"),
    (6, "BlackBerry OS"),
    (7, "Mac OS X"),
    (8, "Ubuntu"),
    (9, "Symbian OS"),
    (10, "Linux"),
    (11, "Chrome OS"),
    (12, "Harmony OS"),
    (13, "Other")
]

DEVICE_OS_FAMILY_HASHMAP = {
    "iOS": 1,
    "Android": 2,
    "BlackBerry Tablet OS": 3,
    "Windows Phone": 4,
    "Windows": 5,
    "BlackBerry OS": 6,
    "Mac OS X": 7,
    "Ubuntu": 8,
    "Symbian OS": 9,
    "Linux": 10,
    "Chrome OS": 11,
    "Harmony OS": 12,
    "Other": 13
}


class DeviceLoginManager(models.Manager):
    """
    Get and Create Device Login Data
    """

    def get_or_create(self, user, request, device_id=None):
        """
        :param device_id:
        :param user: User Model
        :param request:
        :return:
        """
        # IP Address
        ip_address = get_client_ip(request)
        # Os Family
        device_os_family = request.user_agent
        device_os_type = DEVICE_OS_FAMILY_HASHMAP.get(device_os_family, 13)

        # Check if login data is available for that user
        if device_id:

            login_data = self.filter(user=user,
                                     id=device_id,
                                     ip_address=ip_address
                                     )

            # If login data exists return
            if login_data.exists():
                return login_data.first()

        login_data = self.create(
            user=user,
            device_uid=uuid.uuid4(),
            device_os_type=device_os_type,
            device_os_family=device_os_family,
        )
        return login_data


# User Device Login Details
class DeviceLogin(models.Model):
    # User Account
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # Device UID
    device_uid = models.UUIDField(unique=True)
    # Device Type
    device_os_type = models.IntegerField(choices=DEVICE_OS_TYPE)
    # Device Name
    device_os_family = models.CharField(max_length=126)
    # IP Address
    ip_address = models.CharField(max_length=50)
    # First Login
    first_login = models.DateTimeField(auto_now_add=True, editable=False)
    # Login Time
    last_login = models.DateTimeField(auto_now=True)

    objects = DeviceLoginManager()
