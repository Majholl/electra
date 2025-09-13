from django.urls import path 
from .views import homePage, LoginPage, RegisterPage,  registerUser, loginUser, logoutUser , superadminpage


urlpatterns = [
    path('home', homePage, name='HomePage'),
    path('', homePage, name='HomePage'),
    path('authentication/', LoginPage, name='AuthLogin'),
    path('authentication/register', RegisterPage, name='AuthRegister'),
    
    
    
    path('login', loginUser, name='loginToSystem'),
    path('logout', logoutUser, name='logoutFromSystem'),
    path('superadminpage', superadminpage, name='adminpage'),
    
    path('register', registerUser, name='register'),
]