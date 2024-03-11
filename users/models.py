from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

from core.models import Grade, Board


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    USER_TYPE_CHOICES = [
        (0, 'Admin'),
        (1, 'Student'),
    ]
    type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['type']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    grade = models.ForeignKey(Grade, null=True, blank=True, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, null=True, blank=True, on_delete=models.CASCADE)
