from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, name, terms, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, terms and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), name=name, terms=terms)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, terms, password=None, password2=None):
        """
        Creates and saves a superuser with the given email, name, terms and password.
        """
        user = self.create_user(email, name=name, terms=terms, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email Address", max_length=255, unique=True)
    name = models.CharField(max_length=200)
    terms = models.BooleanField()
    date_of_birth = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "terms"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
