from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

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

    
    national_code = models.BigIntegerField('Code meli of the user', unique=True, null=False)
    
    email = models.EmailField('Email address', db_index=True, unique=True)
    profile = models.ImageField('User profile', upload_to=UserProfile, null=True)
    phone_number = PhoneNumberField('Phone Number' , max_length=30 , unique=True, null=True)
    
    usertype = models.CharField('User type', max_length=10, choices=UserType.choices, default=UserType.USER)
        
    otp = models.CharField('One time password', max_length=6, null=True)
    otp_expire_time = models.DateTimeField('One time password expiration', null=True, blank=True)
    otp_attempt = models.IntegerField('One time password attempt', default=0)
    
    account_status = models.CharField('Account status', max_length=8, choices=AccountStatus.choices, default=AccountStatus.DEACTIVE)
    is_active = models.BooleanField('Account activation', default=0)    
    
    maxpanelcount = models.SmallIntegerField('Number of panel careation by admins', default=0)
    allowunlimitpanelcreation = models.BooleanField('Allow admin to create panel', default=0)    
    
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'national_code', 'password']
    
    objects = CustomUserManger()
    
    class Meta:
        verbose_name = 'User'
        db_table = 'users'
        ordering = ['-created_at']
        
        
        
    def set_otp(self, code:str):
        self.otp = code
        self.otp_expire_time = timezone.now() + settings.OTP_EXPIRE_TIME
        self.save()    
    
    
    @property 
    def clear_otp(self):
        self.otp = None
        self.save()
   
           
    @property
    def validate_otp_expiration(self):
        return (timezone.now() - self.otp_expire_time) <= settings.OTP_EXPIRE_TIME

   
    @property
    def otp_attempt_count(self):
        if self.otp_attempt <4:
            self.otp_attempt +=1 
        if self.otp_attempt >= 3 :
            self.account_status = Users.AccountStatus.LOCKED
        self.save()        
        

    @property
    def otp_code_expiration(self):
        self.otp = None
        self.otp_expire_time = None
        self.otp_attempt = 0 
        self.save()    







class GroupUserAdminModel(models.Model):
    user = models.ForeignKey(verbose_name='The user itself', to=Users, on_delete= models.RESTRICT, related_name='user_relation_to_admin')
    relatedtoadmin = models.ForeignKey(verbose_name='The user who related to', to=Users, on_delete= models.RESTRICT, related_name='admin_relation_to_user')    
    
    class Meta :
        verbose_name = 'User-Groups'
        db_table = 'usersgroups'
        
        