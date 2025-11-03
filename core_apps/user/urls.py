from django.urls import path 

from .views import (
                homePage,
                LoginPage, RegisterPage, loginUser,  logoutUser ,
                AdminDashboard, NotFound404, ServerError500,
                admins_list, load_selected_admin, modify_selected_admin, new_admin_list, PromoteUsertoAdmin,
                UserPanel,
                
                
                #//
                load_page_register_user_by_admin,
                register_user_by_admin, 
                verify_otp_page, verify_otp
                
                
                )




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
    path('admins/', admins_list, name='AdminsList'),
    path('admins/<int:page_num>', admins_list, name='AdminsList'),
    path('admin/<int:id>', load_selected_admin, name='LoadSelectedAdmin'), 
    path('admin/modifyadmin/', modify_selected_admin, name='ModifySelectedAdmin'),
    path('admins/add', new_admin_list, name='AddNewAdminList'),
    path('admins/promote', PromoteUsertoAdmin, name='AddNewAdmin'),
    path('panel/', UserPanel, name='UserPanel'),
   
   
   
   
   
   
   
    
    
    
#// 
    path('register', load_page_register_user_by_admin, name='load-page-register-user-by-admin'),
    path('register/submit', register_user_by_admin, name='register-user-by-admin'),
    
    path('verify/otp', verify_otp_page, name='verify-user-otp-page'),
    path('verify/otp/submit', verify_otp, name='verify-user-otp')
]                
