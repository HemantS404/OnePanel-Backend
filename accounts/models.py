from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser):
    name = models.CharField(max_length = 20)
    email = models.EmailField(unique = True)

    email_token =  models.CharField(max_length = 250, null = True, blank = True)
    password_reset_token = models.CharField(max_length = 250, null = True, blank = True)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    is_email_verified = models.BooleanField(default = False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email+', '+self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    def is_verified(self):
        return self.is_email_verified