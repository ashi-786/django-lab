from __future__ import unicode_literals # must occur at the beginning
from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager
from django.utils.translation import gettext_lazy as _

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('First Name'), max_length=250, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=250, blank=True)
    email = models.EmailField(_('Email Address'), unique=True, db_index=True)
    ppic = models.ImageField(_('Profile Picture'), upload_to='img/', blank=True, null=True)

    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff'), default=False)
    # timezone = models.CharField(_('Timezone'), max_length=255, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    username = models.CharField(_('username'), max_length=150, unique=True, blank=True, null=True, db_index=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Removed 'username', 'first_name', 'last_name'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email