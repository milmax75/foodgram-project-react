from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_username
from django.db.models import Q


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
    first_name = models.TextField(max_length=150, blank=False, null=False)
    last_name = models.TextField(max_length=150, blank=False, null=False)
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=10,
                            choices=ROLE_CHOICES,
                            default='user')

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return self.user


class Follow(models.Model):
    user = models.ForeignKey(
        UserCustomized,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='User'
    )
    author = models.ForeignKey(
        UserCustomized,
        on_delete=models.CASCADE,
        related_name='followed',
        verbose_name='Post author'
    )

    class Meta:
        '''Prohibition to create multiple identical subscriptions.
           Prohibition to subscribe to yourself.'''
        constraints = (
            models.UniqueConstraint(fields=('user_id', 'author_id'),
                                    name='unique_following'),
            models.CheckConstraint(check=~Q(user=Q('author')), name='no_selfy')
        )

    def __str__(self):
        return self.user
