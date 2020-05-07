# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
import time
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


# class User(md.User):
# class User(md.User, md.PermissionsMixin):
#
#     def __str__(self):
#         return "@{}".format(self.username)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    mobile_number = PhoneNumberField(blank=True)
    is_employee = models.BooleanField(default=False)
    is_handyman = models.BooleanField(default=False)
    job = models.CharField(max_length=50)
    address = models.CharField(max_length=200, default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_handyman_status(self):
        return self.is_handyman

    def get_cache_name(self):
        return self.name

    def get_first_name(self):
        return self.name.split()[0]

    def get_date_joined_short(self):
        return self.date_joined.strftime('%d %b %Y')

#
# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     username=models.CharField(blank=True, null=True)
#     REQUIRED_FIELDS = ['email', 'username']
#     mobile_number = PhoneNumberField(unique=True)
#
#     def __str__(self):
#         return self.email
