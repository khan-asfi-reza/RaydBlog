from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from utils.model_utils import has_chars, username_validator


class UserManager(BaseUserManager):
    """
    Returns Active Users
    """

    def get_queryset_all(self):
        self.get_active_users()

    def get_active_users(self):
        return self.filter(is_active=True)

    # Create User Method
    def __create_user(self, username, email, password, phone_number, phone_number_ccode, **kwargs):
        if not email or not phone_number or not phone_number_ccode:
            raise ValueError('Users must have an email address and a phone number')

        if has_chars(phone_number):
            raise ValidationError({
                "phone_number": "Invalid Phone number, cannot contain any alphabet"
            })

        if phone_number_ccode[0] != "+" and has_chars(phone_number_ccode):
            raise ValidationError({
                "phone_number": "Invalid Phone Number Code"
            })

        if not username_validator(username):
            raise ValidationError({
                "user": "Username can only contain alphabets, numbers and underscores"
            })

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            phone_number_ccode=phone_number_ccode,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create Normal User
    def create_user(self, username, email, password, phone_number, phone_number_ccode, **kwargs):
        return self.__create_user(username, email, password, phone_number, phone_number_ccode, **kwargs)

    # Create Admin Users
    def create_superuser(self, username, email, password, phone_number, phone_number_ccode, **kwargs):
        return self.__create_user(
            username,
            email,
            password,
            phone_number,
            phone_number_ccode,
            is_staff=True,
            is_active=True,
            is_superuser=True,
            **kwargs,
        )

    def create_staff(self, username, email, password, phone_number, phone_number_ccode, **kwargs):
        return self.__create_user(
            username,
            email,
            password,
            phone_number,
            phone_number_ccode,
            is_staff=True,
            is_active=True,
            is_superuser=False,
            **kwargs, )

    # Returns Admin Staff Users
    def get_admin_staff_users(self):
        return self.filter(Q(is_staff=True) | Q(is_superuser=True))

    # Get or create
    def get_or_new(self, **kwargs):
        # Get username and password
        username = kwargs.get("username", "")
        password = kwargs.get("password", "")
        # If username
        if username:
            is_created = False
            # Get Filtered data to see existing data
            filtered_data = self.filter(username=username)
            if filtered_data.exists():
                # If exists update the existing
                user = filtered_data.first()
            else:
                # Otherwise create data
                user = self.create_user(**kwargs)
                is_created = True

            return user, is_created
        raise ValidationError({"username": "Invalid username"})


class User(AbstractUser):
    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15, verbose_name="User Phone Number")
    phone_number_ccode = models.CharField(max_length=6, verbose_name="Phone Number Country Code")

    verified = models.BooleanField(default=False, verbose_name="User Profile Verified")
    # Date of birth
    date_of_birth = models.DateField(verbose_name="Date of birth", null=True, blank=True)

    REQUIRED_FIELDS = ("email", 'phone_number', 'phone_number_ccode')
    objects = UserManager()

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    @property
    def phone_number_full(self):
        return self.phone_number_ccode + self.phone_number

    def clean(self):
        if has_chars(self.phone_number):
            raise ValidationError({
                "phone_number": "Invalid Phone number, cannot contain any alphabet"
            })

        if self.phone_number_ccode[0] != "+" and has_chars(self.phone_number_ccode):
            raise ValidationError({
                "phone_number": "Invalid Phone Number Code"
            })

        if not username_validator(self.username):
            raise ValidationError({
                "user": "Username can only contain alphabets, numbers and underscores"
            })

    def deactivate_user(self):
        """
        Deactivates a user
        :return:
        """
        self.is_active = False
        self.save()

    def activate_user(self):
        """
        Activates a user
        :return:
        """
        self.is_active = True
        self.save()

    def verify_user(self):
        """
        Verifies a user

        :return:None
        """
        if not self.verified:
            self.verified = True
            self.save()

    class Meta:
        unique_together = ["phone_number", "phone_number_ccode"]
