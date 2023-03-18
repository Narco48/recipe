from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from utils.BaseModel import DateMixin 
# Create your models here.



class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError('Users should have a username')
        if password is None:
            raise TypeError('Password should not be none')
       
        user = self.model(username=self.normalize_email(username), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError('Users should have a Username')
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin,DateMixin):
    
    fullname = models.CharField(max_length=255,null=True, blank=True)  # User Fullname
    username = models.CharField(max_length=255,null=True, blank=True, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    mobile_no = models.BigIntegerField(unique=True,null=True, blank=True)  # User contact no.
    gender = models.CharField(max_length=10,null=True,blank=True)
    otp = models.IntegerField(null=True, blank=True)   # email verification otp
    img= models.ImageField(upload_to="profile", height_field=None, width_field=None, max_length=None,null=True,blank=True)
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username


