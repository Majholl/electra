from django.contrib.auth.models import AbstractUser
from django.db import models
from os import path
from time import time


from .manager import CustomUserManger



def UserProfile(instance, filename):
    try :
        split_name = path.splitext(filename)
        file_name = f'{instance.username}_{int(time())}{split_name[-1]}'
        return path.join('UserProfile', file_name)
    except Exception as err:
        print(f'Error saving user profile image name | user_id : {instance.pk} | {str(err)}')
        
         
         
          
class Users(AbstractUser):
    
    class UserType(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'
        SUPERADMIN = 'superadmin', 'Superadmin'
    
    class AccountStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        DEACTIVE = 'deactive', 'Deactive'
        LOCKED = 'locked', 'Locked'



    email = models.EmailField('Email address', db_index=True, unique=True)
    profile = models.ImageField('User profile', upload_to=UserProfile, null=True)
    usertype = models.CharField('User type', max_length=10, choices=UserType.choices, default=UserType.USER)
    account_status = models.CharField('Account status', max_length=8, choices=AccountStatus.choices, default=AccountStatus.DEACTIVE)
    is_active = models.BooleanField('Account activation', default=0)
    
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']
    
    objects = CustomUserManger()
    
    class Meta:
        verbose_name = 'User'
        db_table = 'users'
        ordering = ['-created_at']
        
        