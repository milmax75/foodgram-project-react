from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_username


class UserCustomized(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(max_length=150,
                                unique=True,
                                validators=(validate_username,))
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.TextField(max_length=150)
    last_name = models.TextField(max_length=150)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=10,
                            choices=ROLE_CHOICES,
                            default='user')

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser
