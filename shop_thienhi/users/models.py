from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Virtual Run API."""
    class GenderChoice(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        OTHER = 'Other', 'Other'

    class UserTypeChoice(models.TextChoices):
        STAFF = 'Staff', 'Staff'            # Bán hàng
        STOCKER = 'Stocker', 'Stocker'      # Quản lý kho, sản phấm
        MANAGER = 'Manager', 'Manager'      # Quản lý shop

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=8, null=True, blank=True, choices=GenderChoice.choices)
    avatar = models.ImageField(null=True, blank=True)
    user_type = models.CharField(max_length=20, null=True, blank=True,
                                 choices=UserTypeChoice.choices, default=UserTypeChoice.STAFF)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Customer(models.Model):

    class GenderChoice(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        OTHER = 'Other', 'Other'
    
    class AttachmentLevelChoice(models.TextChoices):
        LEVEL_1 = 'Level_1', 'Level_1'
        LEVEL_2 = 'Level_2', 'Level_2'
        LEVEL_3 = 'Level_3', 'Level_3'
        LEVEL_4 = 'Level_4', 'Level_4'

    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, unique=True)
    gender = models.CharField(max_length=8, null=True, choices=GenderChoice.choices)
    number_of_transactions = models.IntegerField(default=0, null=True)
    total_money = models.FloatField(default=0, null=True)
    attachment_level = models.CharField(max_length=8, null=True, choices=AttachmentLevelChoice.choices)     # Mức độ gắn bó
    age = models.IntegerField(default=20, null=True)
