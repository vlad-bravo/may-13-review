from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)
