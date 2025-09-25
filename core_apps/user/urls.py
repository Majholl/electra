from django.urls import path 
from .views import (
                homePage,
                LoginPage, RegisterPage, loginUser,  logoutUser ,
                AdminDashboard, NotFound404, ServerError500,
                admins_list, load_selected_admin, modify_selected_admin, addnewadmins_list, addnewadmin,
                registerUser, 
                userpanel)


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



#//
    path('modifyadmin/', modify_selected_admin, name='ModifySelectedAdmin'),
    
    
    
    
    
    
    
    
    path('addnewadminlist', addnewadmins_list, name='addnewadminlist'),
    path('addnewadmin', addnewadmin, name='addnewadmin'),
 
 
    path('superadminpage', AdminDashboard, name='adminpage'),
    path('register', registerUser, name='register'),
    
    path('panel', userpanel, name='userpanel')
]                
