from django.urls import path 

from .views import (
                homePage,
                LoginPage, RegisterPage, loginUser,  logoutUser ,
                AdminDashboard, NotFound404, ServerError500,
                
                
                
                #// Admins promotion & modifying modules //# 
                registerNewAdmin, submitRegisterNewAdmin,
                adminsList, loadSelectedAdmin, modifySelectedAdmin, newAdminList, promoteUserToAdmin,
                
                UserPanel,
                
                #//
                loadAddUserPage_byAdmin,
                registerUser_byadmin, 
                load_selected_user_byadmin,
                
                
                verify_otp_page, verify_otp
                
                
    )
from .searchs import findOnSearchToadmin



urlpatterns = [
    path('home', homePage, name='HomePage'),
    path('', homePage, name='HomePage'),
    path('authentication/', LoginPage, name='AuthLogin'),
    path('authentication/register', RegisterPage, name='AuthRegister'),
    path('login', loginUser, name='loginToSystem'),
    path('logout', logoutUser, name='logoutFromSystem'),
    path('dashboard/', AdminDashboard, name='AdminDashboard'),
    path('404/', NotFound404, name='404-nf'),
    path('server-error/', ServerError500, name='500-se'),
    
    
    #// Admins promotion & modifying urls 
    path('admins/', adminsList, name='AdminsList'),
    path('registernewadmin/',registerNewAdmin, name='RegisterNewAdmin' ),
    path('submitRegisterNewAdmin', submitRegisterNewAdmin, name='SubmitRegisterNewAdmin'),
    path('admins/<int:page_num>', adminsList, name='AdminsList'),
    path('admin/<int:id>', loadSelectedAdmin, name='LoadSelectedAdmin'), 
    path('admin/modifyadmin/', modifySelectedAdmin, name='ModifySelectedAdmin'),
    path('admins/add', newAdminList, name='AddNewAdminList'),
    path('admins/promote', promoteUserToAdmin, name='AddNewAdmin'),
    
    
    #// search boxs
    path('findusertoadmin/', findOnSearchToadmin, name = 'FindUserToadmin' ),
    
    
    path('panel/', UserPanel, name='UserPanel'),
   
   
   
   
   
   
    path('register/user', loadAddUserPage_byAdmin, name='LoadAddUserPage'),
    path('register/submit', registerUser_byadmin, name='RegisterUserByadmin'),
    path('admin/user/<int:id>/', load_selected_user_byadmin, name='LoadUserOfAdmin'),
    
    
    
#// 
    
    path('verify/otp', verify_otp_page, name='verify-user-otp-page'),
    path('verify/otp/submit', verify_otp, name='verify-user-otp')
]                
