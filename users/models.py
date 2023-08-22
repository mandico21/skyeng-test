from django.contrib.auth.models import AbstractUser
from django.db import models


class UserABC(AbstractUser):
    email = models.EmailField(
        verbose_name='Почта',
        unique=True,
        blank=False,
        null=False
    )
