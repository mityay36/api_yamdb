from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        username,
        email,
        password="",
        bio="",
        role="user",
        first_name="",
        last_name="",
    ):
        if username is None:
            raise TypeError("Users must have a username.")

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            confirmation_code=self.make_random_password(length=12),
            password=password,
            role=role,
            bio=bio,
            first_name=first_name,
            last_name=last_name,
        )
        user.save()

        return user

    def create_superuser(
        self,
        username,
        email,
        password=None,
        bio="",
        role="admin",
        first_name="",
        last_name="",
    ):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(
            username=username,
            email=email,
            password=make_password(password),
            role=role,
            bio=bio,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_superuser = True
        user.is_staff = True
        user.email_user(
            subject="confirmation_code",
            message=user.confirmation_code,
            fail_silently=False,
        )
        user.save()

        return user


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    confirmation_code = models.CharField(max_length=12)
    role = models.CharField(
        choices=Role.choices, max_length=128, default=Role.USER
    )
    bio = models.TextField(blank=True)

    objects = CustomUserManager()

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR
