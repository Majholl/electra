from django.urls import path 
from .views import homePage, LoginPage, RegisterPage, admins_list,   registerUser, loginUser, logoutUser , SuperAdminPage



urlpatterns = [
    path('home', homePage, name='HomePage'),
    path('', homePage, name='HomePage'),
    path('authentication/', LoginPage, name='AuthLogin'),
    path('authentication/register', RegisterPage, name='AuthRegister'),
    
    
    path('dashboard/', SuperAdminPage, name='dashboard-superadmin'),
    path('admins/', admins_list, name='adminsList'),
    path('admins/<int:page_num>', admins_list, name='adminsList'),
    
    
    
    
    path('login', loginUser, name='loginToSystem'),
    path('logout', logoutUser, name='logoutFromSystem'),
    path('superadminpage', SuperAdminPage, name='adminpage'),
    
    path('register', registerUser, name='register'),
]                
