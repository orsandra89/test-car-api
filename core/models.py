from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.deletion import CASCADE


class UserManager(BaseUserManager):

    def create_user(self, email, password = None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creating superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
        

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Carbrand(models.Model):
    """Carbrand object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    brandname = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.brandname


class Carmodel(models.Model):
    """Carmodel object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE
    )
    modelname = models.CharField(max_length=255)
    modelyear = models.IntegerField()
    modelbodystyle = models.CharField(max_length=255)

    def __str__(self):
        return self.modelname