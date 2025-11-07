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


    national_code = models.BigIntegerField('National code', unique=True, null=False)
    phone_number = PhoneNumberField('Phone number' , max_length=30 , unique=True, null=True, region=None)
   
    email = models.EmailField('Email address', unique=False, null=True)
    username = models.CharField('Username', max_length=150, unique=False, null=True)
   
    profile = models.ImageField('User profile', upload_to=UserProfile, null=True)
    usertype = models.CharField('User type', max_length=10, choices=UserType.choices, default=UserType.USER)
    
    account_status = models.CharField('Account status', max_length=8, choices=AccountStatus.choices, default=AccountStatus.DEACTIVE)
    is_active = models.BooleanField('Account activation', default=0)    
        
        
    otp = models.CharField('One time password', max_length=6, null=True)
    otp_expire_time = models.DateTimeField('One time password expiration', null=True, blank=True)
    otp_attempt = models.IntegerField('One time password attempt', default=0)
    
    
    maxpanelcount = models.SmallIntegerField('Number of panel careation by admins', default=0)
    allowunlimitpanelcreation = models.BooleanField('Allow admin to create panel ultimately', default=0)    
    
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']
    USERNAME_FIELD = 'national_code'
    
    
    objects = CustomUserManger()
    
    
    
    class Meta:
        verbose_name = 'User'
        db_table = 'users'
        ordering = ['-created_at']
        
        
    def __str__(self):
        return f"pk :{self.pk}|Name :{str(self.first_name) +'-'+ str(self.last_name)}|UserType :{self.usertype}"  
     
    def set_otp(self, code:str):
        self.otp = code
        self.otp_expire_time = timezone.now() + settings.OTP_EXPIRE_TIME
        self.save()    
    
    
    def verify_otp_code(self, code_otp):
        
        if self.otp == str(code_otp):
            self.otp = None
            self.otp_expire_time = None
            self.otp_attempt = 0
            self.account_status = Users.AccountStatus.ACTIVE
            self.is_active = 1
            self.save()
            return True
        
        return False
            
            
    
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
        
        