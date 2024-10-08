from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser,
    Group,
    Permission,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractUser):
    username = models.CharField(max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = AccountManager()
    groups = models.ManyToManyField(Group, related_name="account_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="account_user_permissions"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
